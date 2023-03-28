"""
Pydantic automation validation.
"""
from __future__ import annotations

import abc
from typing import Annotated, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, conint, conlist, constr, validator
from pydantic.fields import ModelField

from . import enums
from .field_validators import str_is_identifier


# ==== helpers ====
class AutomationModel(BaseModel):
    # noinspection PyMethodParameters
    @validator("*")
    def empty_string_to_none(cls, value, field: ModelField):
        """
        If the field is some sort of `Optional[str]` and the value is an empty string, yield None instead.

        This helps with automation made on the web dashboard, which sets optional fields to empty string rather than
        None.
        """
        if value == "" and field.allow_none and issubclass(field.type_, str):
            return None
        return value


# --- helper types ---
str255 = constr(max_length=255, strip_whitespace=True)
str1024 = constr(max_length=1024, strip_whitespace=True)
str4096 = constr(max_length=4096, strip_whitespace=True)
AnnotatedString255 = str255
AnnotatedString1024 = str1024
AnnotatedString4096 = str4096
IntExpression = str255
AdvantageType = Literal[-1, 0, 1]


# --- Helper Models ---
class HigherLevels(AutomationModel):
    __root__: Dict[constr(regex=r"[0-9]"), str255]


class SpellSlotReference(AutomationModel):
    slot: Union[conint(ge=1, le=9), str255]


class AbilityReference(AutomationModel):
    id: int
    typeId: int


class AttackModel(AutomationModel):
    v: Literal[2] = Field(..., alias="_v")
    name: str255
    automation: ValidatedAutomation
    verb: Optional[str255]
    proper: Optional[bool]
    criton: Optional[int]
    phrase: Optional[str1024]
    thumb: Optional[str255]
    extra_crit_damage: Optional[str255]
    activation_type: Optional[enums.ActivationType]

    def dict(self, *args, **kwargs):
        kwargs["by_alias"] = True
        return super().dict(*args, **kwargs)


# ==== effects ====
class ValidatedAutomation(AutomationModel):  # named to prevent namespace conflicts with actual automation engine
    __root__: List[
        Annotated[
            Union[
                Target,
                Attack,
                Save,
                Damage,
                TempHP,
                LegacyIEffect,
                IEffect,
                RemoveIEffect,
                Roll,
                Text,
                SetVariable,
                Condition,
                UseCounter,
                CastSpell,
                Check,
            ],
            Field(discriminator="type"),
        ]
    ]


class Effect(AutomationModel, abc.ABC):
    type: str
    meta: Optional[ValidatedAutomation]


# --- target ---
class Target(Effect):
    type: Literal["target"]
    target: Union[Literal["all", "each", "self", "parent", "children"], conint(ge=1)]
    effects: ValidatedAutomation
    sortBy: Optional[Literal["hp_asc", "hp_desc"]]


# --- attack ---
class Attack(Effect):
    type: Literal["attack"]
    hit: ValidatedAutomation
    miss: ValidatedAutomation
    attackBonus: Optional[IntExpression]
    adv: Optional[IntExpression]


# --- save ---
class Save(Effect):
    type: Literal["save"]
    stat: Literal["str", "dex", "con", "int", "wis", "cha"]
    fail: ValidatedAutomation
    success: ValidatedAutomation
    dc: Optional[IntExpression]
    adv: Optional[AdvantageType]


# --- damage ---
class Damage(Effect):
    type: Literal["damage"]
    damage: AnnotatedString255
    overheal: Optional[bool]
    higher: Optional[HigherLevels]
    cantripScale: Optional[bool]


# --- temphp ---
class TempHP(Effect):
    type: Literal["temphp"]
    amount: AnnotatedString255
    higher: Optional[HigherLevels]
    cantripScale: Optional[bool]


# --- ieffect ---
# -- helpers --
class PassiveEffects(AutomationModel):
    attack_advantage: Optional[IntExpression]
    to_hit_bonus: Optional[AnnotatedString255]
    damage_bonus: Optional[AnnotatedString255]
    magical_damage: Optional[IntExpression]
    silvered_damage: Optional[IntExpression]
    resistances: Optional[List[AnnotatedString255]]
    immunities: Optional[List[AnnotatedString255]]
    vulnerabilities: Optional[List[AnnotatedString255]]
    ignored_resistances: Optional[List[AnnotatedString255]]
    ac_value: Optional[IntExpression]
    ac_bonus: Optional[IntExpression]
    max_hp_value: Optional[IntExpression]
    max_hp_bonus: Optional[IntExpression]
    save_bonus: Optional[AnnotatedString255]
    save_adv: Optional[List[AnnotatedString255]]
    save_dis: Optional[List[AnnotatedString255]]
    check_bonus: Optional[AnnotatedString255]
    check_adv: Optional[List[AnnotatedString255]]
    check_dis: Optional[List[AnnotatedString255]]


class AttackInteraction(AutomationModel):
    attack: AttackModel
    defaultDC: Optional[IntExpression]
    defaultAttackBonus: Optional[IntExpression]
    defaultCastingMod: Optional[IntExpression]


class ButtonInteraction(AutomationModel):
    automation: ValidatedAutomation
    label: constr(max_length=80, min_length=1, strip_whitespace=True)
    verb: Optional[AnnotatedString255]
    style: Optional[IntExpression]
    defaultDC: Optional[IntExpression]
    defaultAttackBonus: Optional[IntExpression]
    defaultCastingMod: Optional[IntExpression]


class LegacyIEffect(Effect):
    type: Literal["ieffect"]
    name: str255
    duration: IntExpression
    effects: AnnotatedString1024
    end: Optional[bool]
    conc: Optional[bool]
    desc: Optional[AnnotatedString1024]
    stacking: Optional[bool]
    save_as: Optional[str255]
    parent: Optional[str255]

    _save_as_identifier = validator("save_as", allow_reuse=True)(str_is_identifier)


class IEffect(Effect):
    type: Literal["ieffect2"]
    name: AnnotatedString255
    duration: Optional[IntExpression]
    effects: Optional[PassiveEffects]
    attacks: Optional[List[AttackInteraction]]
    buttons: Optional[List[ButtonInteraction]]
    end: Optional[bool]
    conc: Optional[bool]
    desc: Optional[AnnotatedString1024]
    stacking: Optional[bool]
    save_as: Optional[str255]
    parent: Optional[str255]

    _save_as_identifier = validator("save_as", allow_reuse=True)(str_is_identifier)


# --- remove_ieffect ---
class RemoveIEffect(Effect):
    type: Literal["remove_ieffect"]
    removeParent: Optional[Literal["always", "if_no_children"]]


# --- roll ---
class Roll(Effect):
    type: Literal["roll"]
    dice: AnnotatedString255
    name: str255
    higher: Optional[HigherLevels]
    cantripScale: Optional[bool]
    hidden: Optional[bool]
    displayName: Optional[str255]


# --- text ---
class Text(Effect):
    type: Literal["text"]
    text: Union[AbilityReference, constr(max_length=4096, strip_whitespace=True, strict=True)]
    title: Optional[str255]


# --- variable ---
class SetVariable(Effect):
    type: Literal["variable"]
    name: str255
    value: IntExpression
    higher: Optional[HigherLevels]
    onError: Optional[IntExpression]

    _name_identifier = validator("name", allow_reuse=True)(str_is_identifier)


# --- condition ---
class Condition(Effect):
    type: Literal["condition"]
    condition: IntExpression
    onTrue: ValidatedAutomation
    onFalse: ValidatedAutomation
    errorBehaviour: Optional[Literal["true", "false", "both", "neither", "raise"]]


# --- counter ---
class UseCounter(Effect):
    type: Literal["counter"]
    counter: Union[SpellSlotReference, AbilityReference, constr(max_length=255, strip_whitespace=True, strict=True)]
    amount: IntExpression
    allowOverflow: Optional[bool]
    errorBehaviour: Optional[Literal["warn", "raise", "ignore"]]


# --- spell ---
class CastSpell(Effect):
    type: Literal["spell"]
    id: int
    level: Optional[int]
    dc: Optional[IntExpression]
    attackBonus: Optional[IntExpression]
    castingMod: Optional[IntExpression]
    parent: Optional[str255]


# --- check ---
AbilityType = Literal[
    "acrobatics",
    "animalHandling",
    "arcana",
    "athletics",
    "deception",
    "history",
    "initiative",
    "insight",
    "intimidation",
    "investigation",
    "medicine",
    "nature",
    "perception",
    "performance",
    "persuasion",
    "religion",
    "sleightOfHand",
    "stealth",
    "survival",
    "strength",
    "dexterity",
    "constitution",
    "intelligence",
    "wisdom",
    "charisma",
]


class Check(Effect):
    type: Literal["check"]
    ability: Union[conlist(AbilityType, min_items=1), AbilityType]
    contestAbility: Optional[Union[conlist(AbilityType, min_items=1), AbilityType]]
    dc: Optional[IntExpression]
    success: Optional[ValidatedAutomation]
    fail: Optional[ValidatedAutomation]
    contestTie: Optional[Literal["fail", "success", "neither"]]
    adv: Optional[AdvantageType]


# --- misc ---
AttackModel.update_forward_refs()
ValidatedAutomation.update_forward_refs()
