from versa.bin.scorer import find_files, load_score_modules, list_scoring, load_summary
import yaml
import os
import logging
import math

TEST_INFO = {'mcd': 5.045226506332897, 'f0rmse': 20.28100448994277, 'f0corr': -0.07540903652440145, 'sdr': 4.8739529795936445, 'sir': float('inf'), 'sar': 4.8739529795936445, 'si_snr': 1.0702757835388184, 'ci_sdr': 4.873954772949219, 'pesq': 1.572286605834961, 'stoi': 0.0076251088596473275, 'speech_bert': 0.9727544188499451, 'speech_bleu': 0.6699938983346256, 'speech_token_distance': 0.850506056080969, 'utmos': 1.9074358940124512, 'dns_overall': 1.4526059573614438, 'dns_p808': 2.094302177429199, 'plcmos': 3.1603124300638834, 'spk_similarity': 0.8953473567962646}

def info_update():
    
    # find files
    if os.path.isdir("test/test_samples/test2"):
        gen_files = sorted(find_files("test/test_samples/test2"))

    # find reference file
    if os.path.isdir("test/test_samples/test1"):
        gt_files = sorted(find_files("test/test_samples/test1"))

    logging.info("The number of utterances = %d" % len(gen_files))

    with open("egs/codec_16k.yaml", "r", encoding="utf-8") as f:
        score_config = yaml.full_load(f)

    score_modules = load_score_modules(
        score_config,
        use_gt=(True if gt_files is not None else False),
        use_gpu=False,
    )

    assert len(score_config) > 0, "no scoring function is provided"

    score_info = list_scoring(
        gen_files, score_modules, gt_files, output_file=None
    )
    summary = load_summary(score_info)
    print("Summary: {}".format(load_summary(score_info)), flush=True)

    
    for key in summary:
        if math.isinf(TEST_INFO[key]) and math.isinf(summary[key]):
            # for sir"
            continue
        # the plc mos is undeterministic
        if abs(TEST_INFO[key] - summary[key]) > 1e-5 and key != "plcmos":
            raise ValueError("Value issue in the test case, might be some issue in scorer {}".format(key))
    print("check successful", flush=True)


if __name__ == "__main__":
    info_update()
