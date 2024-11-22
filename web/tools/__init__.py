from funasr import AutoModel


class LazyLoader:
    def __init__(self, factory):
        self.factory = factory
        self._value = None

    def generate(self, input_f):
        if self._value is None:
            self._value = self.factory()
        return self._value.generate(input_f)


def expensive_initialization():
    return AutoModel(model="iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
                     vad_model="damo/speech_fsmn_vad_zh-cn-16k-common-pytorch",
                     punc_model="damo/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
                     spk_model="damo/speech_campplus_sv_zh-cn_16k-common",
                     )


funasr_model = LazyLoader(expensive_initialization)

