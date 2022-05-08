import pydantic
import automation_common


def test_format_validation_error():
    try:
        pydantic.parse_obj_as(
            list[automation_common.validation.models.AttackModel],
            [
                {
                    "name": "error test",
                    "automation": [
                        {
                            "target": "each",
                            "effects": [
                                {
                                    "stat": "con",
                                    "dc": "20",
                                    "type": "save",
                                    "success": [],
                                    "fail": [
                                        {
                                            "name": "error test",
                                            "buttons": [
                                                {
                                                    "automation": [
                                                        {
                                                            "target": "self",
                                                            "effects": [
                                                                {
                                                                    "fail": [],
                                                                    "stat": "con",
                                                                    "type": "save",
                                                                    "success": [
                                                                        {
                                                                            "condition": "len(ieffect.children) == 2",
                                                                            "onTrue": [],
                                                                            "type": "condition",
                                                                            "onFalse": [
                                                                                {
                                                                                    "name": "error test",
                                                                                    "stacking": True,
                                                                                    "duration": -1,
                                                                                    "parent": "ieffect",
                                                                                    "type": "ieffect",
                                                                                },
                                                                            ],
                                                                        }
                                                                    ],
                                                                }
                                                            ],
                                                            "type": "target",
                                                        },
                                                    ],
                                                    "label": "error test",
                                                }
                                            ],
                                            "type": "ieffect2",
                                        }
                                    ],
                                }
                            ],
                            "type": "target",
                        },
                    ],
                    "_v": 2,
                }
            ],
        )
    except pydantic.ValidationError as e:
        assert (
            automation_common.validation.utils.format_validation_error(e) == "1 validation error for"
            " ParsingModel[list[automation_common.validation.models.AttackModel]]\n[0].automation[0] ->"
            " Target.effects[0] -> Save.fail[0] -> IEffect.buttons[0].automation[0] -> Target.effects[0] ->"
            " Save.success[0] -> Condition.onFalse[0] -> LegacyIEffect.effects\n  field required"
            " (type=value_error.missing)"
        )
