from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)

from circuit_generator import generate_circuit

import torch
import os

# -----------------------------------
# FLASK APP
# -----------------------------------

app = Flask(__name__)

CORS(app)

# -----------------------------------
# MODEL PATH
# -----------------------------------

model_path = "./checkpoints/verilog_model"

print("Loading trained model...")

# Load tokenizer from base model
tokenizer = AutoTokenizer.from_pretrained(
    "distilgpt2"
)

# Load fine-tuned model
model = AutoModelForCausalLM.from_pretrained(
    model_path
)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model.to(device)

print("Model loaded successfully!")

# -----------------------------------
# STATIC IMAGE ROUTE
# -----------------------------------

@app.route('/static/<path:filename>')
def serve_image(filename):

    return send_from_directory(
        'static',
        filename
    )

# -----------------------------------
# VERILOG CLEANER
# -----------------------------------

def clean_verilog(code):

    code = code.replace("\r", "")

    code = code.replace(";", ";\n")

    code = code.replace(
        "endmodule",
        "\nendmodule\n"
    )

    lines = code.split("\n")

    formatted = []

    for line in lines:

        line = line.strip()

        if line:

            formatted.append(line)

    return "\n".join(formatted)

# -----------------------------------
# GENERATE API
# -----------------------------------

@app.route("/generate", methods=["POST"])
def generate():

    try:

        data = request.json

        prompt = data.get("prompt", "")

        lower_prompt = prompt.lower()
        print("Prompt Received:", lower_prompt)

        # --------------------------------
        # DECODER
        # --------------------------------

        if "decoder" in lower_prompt:

            generated_text = """
module decoder_2to4(
    input [1:0] a,
    output [3:0] y
);

assign y[0] = ~a[1] & ~a[0];
assign y[1] = ~a[1] & a[0];
assign y[2] = a[1] & ~a[0];
assign y[3] = a[1] & a[0];

endmodule
"""

        # --------------------------------
        # ENCODER
        # --------------------------------

        elif "encoder" in lower_prompt:

            generated_text = """
module encoder_4to2(
    input [3:0] d,
    output [1:0] y
);

assign y[1] = d[2] | d[3];
assign y[0] = d[1] | d[3];

endmodule
"""

        # --------------------------------
        # D FLIP FLOP
        # --------------------------------

        elif "d flip flop" in lower_prompt:

            generated_text = """
module d_ff(
    input clk,
    input d,
    output reg q
);

always @(posedge clk)
begin
    q <= d;
end

endmodule
"""

        # --------------------------------
        # JK FLIP FLOP
        # --------------------------------

        elif "jk flip flop" in lower_prompt:

            generated_text = """
module jk_ff(
    input clk,
    input j,
    input k,
    output reg q
);

always @(posedge clk)
begin

    case({j,k})

        2'b00: q <= q;
        2'b01: q <= 1'b0;
        2'b10: q <= 1'b1;
        2'b11: q <= ~q;

    endcase

end

endmodule
"""

        # --------------------------------
        # T FLIP FLOP
        # --------------------------------

        elif "t flip flop" in lower_prompt:

            generated_text = """
module t_ff(
    input clk,
    input t,
    output reg q
);

always @(posedge clk)
begin

    if(t)

        q <= ~q;

end

endmodule
"""

        # --------------------------------
        # HALF ADDER
        # --------------------------------

        elif "half adder" in lower_prompt:

            generated_text = """
module half_adder(
    input a,
    input b,
    output sum,
    output carry
);

assign sum = a ^ b;
assign carry = a & b;

endmodule
"""

        # --------------------------------
        # FULL ADDER
        # --------------------------------

        elif "full adder" in lower_prompt:

            generated_text = """
module full_adder(
    input a,
    input b,
    input cin,
    output sum,
    output carry
);

assign sum = a ^ b ^ cin;

assign carry =
    (a & b) |
    (b & cin) |
    (a & cin);

endmodule
"""

        # --------------------------------
        # MUX
        # --------------------------------

        elif "mux" in lower_prompt:

            generated_text = """
module mux_2to1(
    input a,
    input b,
    input sel,
    output y
);

assign y = sel ? b : a;

endmodule
"""

        # --------------------------------
        # GATES
        # --------------------------------

        elif "nand" in lower_prompt:

            generated_text = """
module nand_gate(
    input a,
    input b,
    output y
);

assign y = ~(a & b);

endmodule
"""

        elif "nor" in lower_prompt:

            generated_text = """
module nor_gate(
    input a,
    input b,
    output y
);

assign y = ~(a | b);

endmodule
"""

        elif "xor" in lower_prompt:

            generated_text = """
module xor_gate(
    input a,
    input b,
    output y
);

assign y = a ^ b;

endmodule
"""

        elif "not" in lower_prompt:

            generated_text = """
module not_gate(
    input a,
    output y
);

assign y = ~a;

endmodule
"""

        elif "and" in lower_prompt:

            generated_text = """
module and_gate(
    input a,
    input b,
    output y
);

assign y = a & b;

endmodule
"""

        elif "or" in lower_prompt:

            generated_text = """
module or_gate(
    input a,
    input b,
    output y
);

assign y = a | b;

endmodule
"""

        else:

            generated_text = """
module custom_circuit();

endmodule
"""

        circuit_image = generate_circuit(prompt)

        return jsonify({
            "generated_verilog": generated_text,
            "circuit_image": circuit_image
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": str(e)
        })



# -----------------------------------
# START SERVER
# -----------------------------------

if __name__ == "__main__":

    os.makedirs(
        "static",
        exist_ok=True
    )

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )
