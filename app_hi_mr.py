from flask import Flask, jsonify, request
from flask_cors import CORS

from indicnlp.tokenize import sentence_tokenize, indic_detokenize, indic_tokenize
from indicnlp.normalize.indic_normalize import IndicNormalizerFactory

import codecs
from subword_nmt.apply_bpe import BPE

import ctranslate2

from waitress import serve

from flask_cors import CORS
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False
CORS(app)

## Normalize
factory=IndicNormalizerFactory()
normalizer_hi=factory.get_normalizer("hi")
normalizer_mr=factory.get_normalizer("mr")

bpe_hi = BPE(codecs.open("mt-models/hi-mr/hi-mr/v1.0/bpe-codes/codes.hi", encoding='utf-8'))
bpe_mr = BPE(codecs.open("mt-models/hi-mr/mr-hi/v1.0/bpe-codes/codes.mr", encoding='utf-8'))

translator_himr = ctranslate2.Translator("mt-models/hi-mr/hi-mr/v1.0/model_ct2/", inter_threads=4, intra_threads=1)
translator_mrhi = ctranslate2.Translator("mt-models/hi-mr/mr-hi/v1.0/model_ct2/", inter_threads=4, intra_threads=1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Read input request
        input_json = request.get_json()

        input_config = input_json["config"]
        input_lang = input_config["language"]
        input_src, input_trg = input_lang["sourceLanguage"], input_lang["targetLanguage"]
        
        input_source = input_json["input"]
        output_target = []
        
        for input_text_json in input_source:
            input_text = input_text_json["source"].strip("\n")
            # Paragraphs
            input_paras = input_text.split("\n")
            input_list = [line for line in input_paras if len(line) > 1]

            output=[]
            # Iterate Over Paragraphs
            for paras in input_list:
                if input_src == 'hi':
                    
                    # Split Sentences
                    inp_lines = sentence_tokenize.sentence_split(paras, "hi")

                    # Normalize
                    inp_lines = [normalizer_hi.normalize(line) for line in inp_lines]

                    # Tokenize
                    inp_lines = [' '.join(indic_tokenize.trivial_tokenize(line)) for line in inp_lines]

                    # Apply BPE
                    inp_lines = [bpe_hi.process_line(line).split(" ") for line in inp_lines]

                    # Translate
                    out_lines = translator_himr.translate_batch(inp_lines, beam_size=5, max_batch_size=16)

                    # Remove BPE
                    out_lines = [(' '.join(line.hypotheses[0]) + " ").replace("@@ ", "") for line in out_lines]

                    # Post Processing
                    out_lines = [line.replace('"', '').replace("u200d", "").strip() for line in out_lines]

                    out_lines = [indic_detokenize.trivial_detokenize(line) for line in out_lines]

                elif input_src == 'mr':

                    # Split Sentences
                    inp_lines = sentence_tokenize.sentence_split(paras, "mr")

                    # Normalize
                    inp_lines = [normalizer_mr.normalize(line) for line in inp_lines]

                    # Tokenize
                    inp_lines = [' '.join(indic_tokenize.trivial_tokenize(line)) for line in inp_lines]

                    # Apply BPE
                    inp_lines = [bpe_mr.process_line(line).split(" ") for line in inp_lines]

                    # Translate
                    out_lines = translator_mrhi.translate_batch(inp_lines, beam_size=5, max_batch_size=16)

                    # Remove BPE
                    out_lines = [(' '.join(line.hypotheses[0]) + " ").replace("@@ ", "") for line in out_lines]

                    # Post Processing
                    out_lines = [line.replace('"', '').replace("u200d", "").strip() for line in out_lines]

                    out_lines = [indic_detokenize.trivial_detokenize(line) for line in out_lines]


                output.append(out_lines)

            output_text = '\n'.join([' '.join(lines) for lines in output])

            output_target_json = {}
            output_target_json["source"] = input_text
            output_target_json["target"] = output_text

            output_target.append(output_target_json)


        response_body = {
            "config": input_config,
            "output": output_target
            }
        return jsonify(response_body), 201

    else:
        if request.method == 'GET':
            response_body = {
                "config": None,
                "output": ""
            }
        else:
            response_body = {
                 "config": input_config,
                    "output": " "
                    }
        return jsonify(response_body), 400
        
if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=8003, debug=True)
    serve(app, host='0.0.0.0', port=8003)
    