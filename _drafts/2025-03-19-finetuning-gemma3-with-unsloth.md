https://www.reddit.com/r/LocalLLaMA/comments/1jf10ar/gemma_3_grpo_now_in_unsloth_bug_fixes/

Gemma 3 GRPO now in Unsloth + Bug Fixes

Resources
Hey r/LocalLLaMA! We collabed with Hugging Face to create a free notebook to train your own reasoning model using Gemma 3 and GRPO & also did some fixes for training + inference

Some frameworks had large training losses when finetuning Gemma 3 - Unsloth should have correct losses!
We worked really hard to make Gemma 3 work in a free Colab T4 environment after inference AND training did not work for Gemma 3 on older GPUs limited to float16. This issue affected all frameworks including us, transformers, vLLM etc.
Note - it's NOT a bug in Gemma 3 - in fact I consider it a very cool feature!! It's the first time I've seen this behavior, and it's probably maybe why Gemma 3 seems extremely powerful for it's size!
I found that Gemma 3 had infinite activations if one uses float16, since float16's maximum range is 65504, and Gemma 3 had values of 800,000 or larger. Llama 3.1 8B's max activation value is around 324.
r/LocalLLaMA - Gemma 3 GRPO now in Unsloth + Bug Fixes
Unsloth is now the only framework which works in FP16 machines for Gemma 3 inference and training. This means you can now do GRPO, SFT, FFT etc. for Gemma 3, in a free T4 GPU instance on Colab via Unsloth!
Please update Unsloth to the latest version to enable many many bug fixes, and Gemma 3 finetuning support via pip install --upgrade unsloth unsloth_zoo
Read about our Gemma 3 fixes + details here!
This fix also solved an issue where training loss was not calculated properly for Gemma 3 in FP16.
We picked Gemma 3 (1B) for our GRPO notebook because of its smaller size, which makes inference faster and easier. But you can also use Gemma 3 (4B) or (12B) just by changing the model name and it should fit on Colab.

For newer folks, we made a step-by-step GRPO tutorial here. And here's our Colab notebooks:

GRPO: Gemma 3 (1B) Notebook - long link here: https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/HuggingFace%20Course-Gemma3_(1B)-GRPO.ipynb
Normal SFT: Gemma 3 (4B) Notebook
Happy tuning and let me know if you have any questions! :)


Obviously, two Gigabyte Aorus Waterforce 5090s.

ASUS ProArt Z890-CREATOR motherboard.

Intel Core Ultra 285K.

128GB Corsair Vengance RAM.

Two 4TB WD Black NVMe drives.

Seasonic Prime PX-2200W PSU.

NZXT H9 Flow case.