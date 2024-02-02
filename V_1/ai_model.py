# This is to be used as API for different agents

# Geohot stuff

from io import StringIO
from contextlib import redirect_stdout
from tinygrad import Tensor, nn
from tinygrad.helpers import Timing, colored, getenv, fetch
from extra.models.llama import Transformer, convert_from_huggingface
from sentencepiece import SentencePieceProcessor

class AIRA:
    def create_fixed_tokenizer(self, output_file):
        print("creating fixed tokenizer")
        import extra.junk.sentencepiece_model_pb2 as spb2
        mp = spb2.ModelProto()
        mp.ParseFromString(fetch("https://huggingface.co/teknium/OpenHermes-2.5-Mistral-7B/resolve/main/tokenizer.model?download=true").read_bytes())
        mp.pieces.append(spb2.ModelProto.SentencePiece(piece="<|im_end|>", score=0))
        mp.pieces.append(spb2.ModelProto.SentencePiece(piece="<|im_start|>", score=0))
        with open(output_file, "wb") as f:
            f.write(mp.SerializeToString())

    def create_model_cache(self,output_file, model):
        print(f"creating model cache at {output_file}")
        with Timing("download weights: "):
            part1 = nn.state.torch_load(fetch("https://huggingface.co/teknium/OpenHermes-2.5-Mistral-7B/resolve/main/pytorch_model-00001-of-00002.bin?download=true"))
            part2 = nn.state.torch_load(fetch("https://huggingface.co/teknium/OpenHermes-2.5-Mistral-7B/resolve/main/pytorch_model-00002-of-00002.bin?download=true"))

        with Timing("weights -> model: "):
            nn.state.load_state_dict(model, convert_from_huggingface(part1, model, 32, 8), strict=False)
            nn.state.load_state_dict(model, convert_from_huggingface(part2, model, 32, 8), strict=False)

        with Timing("saving float16 cache: "):
            nn.state.safe_save(nn.state.get_state_dict(model), output_file)

        print("cache created, rerun to use")
        exit(0)

    def __init__(self):
        Tensor.no_grad = True

        with Timing("create model: "):
            model = Transformer(4096, 14336, n_heads=32, n_layers=32, norm_eps=1e-5, vocab_size=32002, n_kv_heads=8, max_context=4096)

        cached_model = "/tmp/cached_openhermes.safetensors"
        if not os.path.isfile(cached_model): self.create_model_cache(cached_model, model)
        with Timing("loading float16 cache: "):
            nn.state.load_state_dict(model, nn.state.safe_load(cached_model))

        if not os.path.isfile("/tmp/tokenizer.model"): self.create_fixed_tokenizer("/tmp/tokenizer.model")
        self.spp = SentencePieceProcessor(model_file="/tmp/tokenizer.model")

        IM_END = 32000
        IM_START = 32001
        def encode_prompt(k, v): return [IM_START] + self.spp.encode(f"{k}\n{v}") + [IM_END] + self.spp.encode("\n")
        def start_prompt(k): return [IM_START] + self.spp.encode(f"{k}\n")
        
    
        toks = [self.spp.bos_id()] + encode_prompt("system", "You are AIRA, an AI powered chatbot ready to assist the user. You are friendly, super entertaining, funny and sarcastic. Your primary purpose is to entertain the user, while making sure to answer the questions asked. ")
        PROMPT = getenv("PROMPT", 1)
        temperature = getenv("TEMP", 0.7)

        start_pos = 0
        outputted = self.output("", toks, "green")
        self.turn = True
        self.PROMPT = PROMPT
        self.encode_prompt = encode_prompt
        self.start_prompt = start_prompt
        self.temperature = temperature
        self.model = model
        self.IM_END = IM_END
        self.IM_START = IM_START
        self.toks = toks
        self.outputted = outputted
        self.start_pos = start_pos
        
    def output(self, outputted, toks, color):
        cur = self.spp.decode(toks)[len(outputted):]
        # sys.stdout.write(colored(cur, color))
        # sys.stdout.flush()
        outputted += cur
        return outputted
        
        
    def run(self, text):
        if self.PROMPT:
            self.toks += self.encode_prompt("user", text) + self.start_prompt("assistant")
        else:
            self.toks += self.start_prompt("user" if self.turn else "assistant")
            self.turn = not self.turn
        old_output_len = len(self.outputted)
        while 1:
            tok = self.model(Tensor([self.toks[self.start_pos:]]), self.start_pos, self.temperature).multinomial().item()
            self.start_pos = len(self.toks)
            # print(self.spp.decode(self.toks)[:len(self.outputted)])
            yield self.spp.decode(self.toks)[:len(self.outputted)]
            self.toks.append(tok)
            self.outputted = self.output(self.outputted, self.toks, "blue" if not self.turn else "cyan")
            if tok == self.IM_END: break
            if tok == self.spp.eos_id(): break
            new_output = self.outputted[old_output_len:]
        
        # out = new_output.split('<|im_start|>')[-1][11:]
        return False # just the output as str
                
if __name__ == '__main__'                :
    mod = AIRA()
    for i in range(2):
        gen = mod.run('who is jon jones')
        next_word = ''
        while True:
            try:
                old_len = len(next_word)
                
                next_word = next(gen)
                # if not next_word: # Not needed as try is used
                #     break
                print(next_word[old_len:], end='')
            except StopIteration:
                break

            
 