
import os
import schemdraw
import schemdraw.logic as logic
import schemdraw.elements as elm


def generate_circuit(prompt):

    prompt = prompt.lower()

    base_dir = os.path.dirname(__file__)

    static_dir = os.path.join(
        base_dir,
        "static"
    )

    os.makedirs(
        static_dir,
        exist_ok=True
    )

    image_path = os.path.join(
        static_dir,
        "circuit.svg"
    )

    d = schemdraw.Drawing()

    # --------------------------------
    # COMPLEX CIRCUITS FIRST
    # --------------------------------

    if "half adder" in prompt:

        d += elm.Box(
            w=4,
            h=2,
            label="HALF\nADDER"
        )

    elif "full adder" in prompt:

        d += elm.Box(
            w=4,
            h=2,
            label="FULL\nADDER"
        )

    elif "mux" in prompt:

        d += elm.Box(
            w=4,
            h=2,
            label="2:1\nMUX"
        )

    elif "decoder" in prompt:

        d += elm.Box(
            w=4,
            h=2,
            label="2:4\nDECODER"
        )

    elif "encoder" in prompt:

        d += elm.Box(
            w=4,
            h=2,
            label="4:2\nENCODER"
        )

    elif "d flip flop" in prompt:

        d += elm.Box(
            w=4,
            h=2,
            label="D\nFF"
        )

    elif "jk flip flop" in prompt:

        d += elm.Box(
            w=4,
            h=2,
            label="JK\nFF"
        )

    elif "t flip flop" in prompt:

        d += elm.Box(
            w=4,
            h=2,
            label="T\nFF"
        )

    # --------------------------------
    # BASIC GATES
    # --------------------------------

    elif "nand" in prompt:

        d += logic.Nand()

    elif "nor" in prompt:

        d += logic.Nor()

    elif "xor" in prompt:

        d += logic.Xor()

    elif "not" in prompt:

        d += logic.Not()

    elif "and" in prompt:

        d += logic.And()

    elif "or" in prompt:

        d += logic.Or()

    else:

        d += elm.Box(
            w=4,
            h=2,
            label="UNKNOWN"
        )

    d.save(image_path)

    print("Circuit Saved:", image_path)

    return "/static/circuit.svg"

