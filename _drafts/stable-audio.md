Slogan: Create music with AI.

- Generative AI is increasingly multi modal. It started with images (Stable Diffusion) and text (GPT), now you can also generate audio, music and even video.
- Stable Audio is a music and audio generation service by Stability AI.
- Stability AI is best known for Stable Diffusion.
- Their mission is to Empower creators with tools that aid creativity.
- In this episode I want to look at how Stable Audio helps creating music and audio.
- you find Stable Audio's beautifully designed website at www.stableaudio.com.
- They provide many examples so you can get an idea what it can do for you.
- To use it you'll need to register an account.
- There is no open source model available, yet, but Stability AI is working on it according to a Reddit post, although it can take some time, as it also has been promised for the previous version. The code for training and inference is already published.
- a free account is enough to play with it a bit but you can only generate 20 tracks per month.
- Thus I think a paid account is needed to really get a feel for it. I bought one for 12 USD/Month which gives me 500 generations per month.
- You can write text prompts and provide audio as input and get audio as result. (text to music, audio to audio)
- It can create tracks of up to 3 minutes with musical structure including intro, verse, bridge, refrain, etc.
- stereo
- high quality audio 44 kHz
- solo tracks
- sound effects
- prompt tipps:
- the more detail the better
- set the mood (musical: groovy, rhythmic, emotional: sad, happy, beautiful)
- chose instruments
- set the tempo
- (a tip is to add "high quality" to the prompt)
- you can also add audio
- audio can be used for style transfer, timing, etc.
- for me this is one of it's best features
- you can for example whistle or hum an idea and let Stable Audio generate a track
- vocal input to instrument output
- or for timing (steps?)
- it can act as a virtual folley
- to prevent copyright infringement, Stablility AI uses audio content recognition technology by Audible Magic
- (do I hit it when I input a known song line?)
- then you can also add extra parameters
- Steps (default?) 0-100
- number of results (default?)
- Seed (random or a fixed one for more reproducible results)
- prompt strenght (relative to audio?)
- steps refers to how the model works
- Stable diffusion works by adding controlled noise to a picture in multiple steps
- The steps are small enough so that an AI model (in this case a transformer) can learn to predict the noise which has been added in a step.
- This way the model can learn to reverse the process and generate the original audio based on the noisy version.
- By integrating both audio and text data ( the original audio and matching descriptions in training) the model becomes able to generate audio based on text and audio input.
- The number of steps define how many steps will be used for generation. The fewer the more random or creative the results will be.
- I think the results are impressive and usable.
- Example uses are music creation (flashing out ideas), social media, podcasts, videos (created background tracks or audio effects)
- When you want to use it in film, TV, advertisements, apps and games you need to contact their sales to purchase an enterprise license.
- I like the quality of the results, the look and feel of the service and enjoyed playing with it.
- I think it's a good addition to a content creator's toolbox
- unfortunatly no API yet. I would love to play with multi-agent systems mixing effects, background audio and text to speech.
- Competes with other services like Sumo, which also can create songs with vocals for songtexts.
- While Suno's music is more impressive (with complete vocal tracks), more musically correct (found "wrong" notes in results). But I think Stable Audio is better for creative use. Musicians love granular tools, not infinite stock music that much. Stable Audio can be used more granualar, but there is certainly still room to grow, for example when it would be able to work with musical notations.
- a similar model architecture is also used other multi modal models like OpenAI's SORA which can generate video. It's promising for future developments and local use. Tweet says: 6 GB vRAM for this model is enough.
- Unfortunately, the company Stablility AI has a hart time... The UK based AI company reportedly has only xxx revenue at xxx costs. It was not fully able to pay their cloud bills of ... and even have outstanding tax payments in the UK. XXX, the head of development for Stable Audio left the company after disagreements with the management whether training on copyrighted material can be considered fair use. This is an important topic for Stability AI as they already face lawsuits with Gettys for Stable Diffustion The current Stable Audio model was allegedly trained on xxx material, so users shouldn't worry about copyright claims for audio generation. I hope Stability AI can solve the issues and turn their business into a profitable one. They are innovative player in the industry and have been very generous with open sourcing models and code, despite their comparatively small size.
- for some reason, people don't like to pay for Stability AI services.
- strenght of Stable Diffusion for images: custom trained models by community
- no business model in distributing open weight models, despite their great value.
- That's it for today. I hope you have enjoyed this episode.

The website: https://stableaudio.com/
Emad Mostaque on Twitter: This model tunes super well to individual music libraries and will continue to improve, with open versions also in the works (will be here: https://github.com/Stability-AI/stable-audio-tools) as that dataset is built out building on the diffusion transformer arch & many more innovations. Wen ComfyUI: https://twitter.com/EMostaque/status/1775504692400869453

Edit: the original tweet: https://x.com/StabilityAI/status/1775501906321793266

Edit 2: Emad says 5 Gb VRAM for this model: https://x.com/EMostaque/status/1775516311591833685

Folley: https://x.com/jordiponsdotme/status/1775504901377831066

music https://x.com/dadabots/status/1775522800582762556


code: https://arxiv.org/abs/2404.01226

https://suno-ai.notion.site/Suno-Discord-Commands-5b62a5bf426346ad8355164c9ecb5115
https://github.com/gcui-art/suno-api

Stable Audio is a music generation product built by Stability AI. Stability AI is known for their Stable Diffusion models which have been at the helm enter of the image generation revolution. Stability AI's mission is to empower creators with tools that aid musical creativity. In this post you'll learn about Is Stable Audio a major step on that mission's path and can become as important for the audio world as Stable Diffusion has been for the image world?

Is this usable?

You can use Stable Audio to create original music, sound effects or any other audio based on text input and reference audio files.

to use in your projects - in your commercial projects if you’re a Pro user, or your non-commercial projects if you’re a Basic tier user. For example, you can use the outputs as samples in your own music. [Stable Audio 2.0 Demo](https://stability-ai.github.io/stable-audio-demo/)

It is based on Stable Audio AudioSparx 2.0 model has been designed to generate full tracks with coherent structure at 3 minutes and 10 seconds. Our new model is available for everyone to generate full tracks on our Stable Audio product.

Key features of the model:

Stable Audio 2.0 sets a new standard in AI generated audio, producing high-quality, full tracks with coherent musical structure up to three minutes in length at 44.1KHz stereo.
The new model introduces audio-to-audio generation by allowing users to upload and transform samples using natural language prompts.
Stable Audio 2.0 was exclusively trained on a licensed dataset from the AudioSparx music library, honoring opt-out requests and ensuring fair compensation for creators.

Stable Audio is based on latent diffusion, with its latent defined by a fully-convolutional variational autoencoder. It is conditioned on text prompts as well as timing embeddings, allowing for fine control over both the content and length of the generated music and sounds. Stable Audio is capable of rendering stereo signals of up to 95 sec at 44.1kHz in 8 sec on an A100 GPU. Despite its compute efficiency and fast inference, it is one of the best in two public text-to-music and -audio benchmarks and, differently from state-of-the-art models, can generate music with structure and stereo sounds. [Fast Timing-Conditioned Latent Audio Diffusion](https://arxiv.org/pdf/2402.04825.pdf)

Our dataset consists of 806,284 audios (19,500 hours) containing music (66% or 94%), sound effects (25% or 5%), and instrument stems (9% or 1%), with the corresponding
text metadata from the stock music provider AudioSparx.

How does it compare with the state-of-the-art?

This section discusses Tables 1, 2, and 3. Stable Audio
can outperform the state-of-the-art in audio quality and also
improves text alignment in MusicCaps. Yet, text alignment
is slightly worse in AudioCaps possibly due to the small
amount of sound effects in our training set (Section 4.1).
It is also very competitive at musicality and at generating
correct stereo music signals. 

Model architecture (Research overview)

The architecture of the Stable Audio 2.0 latent diffusion model is specifically designed to enable the generation of full tracks with coherent structures. To achieve this, we have adapted all components of the system for improved performance over long time scales. A new, highly compressed autoencoder compresses raw audio waveforms into much shorter representations. For the diffusion model, we employ a diffusion transformer (DiT), akin to that used in Stable Diffusion 3, in place of the previous U-Net, as it is more adept at manipulating data over long sequences. The combination of these two elements results in a model capable of recognizing and reproducing the large-scale structures that are essential for high-quality musical compositions.

Stable Audio is
also capable to generate structured music: with intro, some
degree of development, and outro. Note that state-of-the-art
models are not consistent at generating a coherent structure,
since they are mainly capable of developing musical ideas.

First, note that latent diffusion (AudioLDM2
and Stable Audio) is significantly faster than autoregressive
modeling, as outlined in the introduction. Second, note that
Stable Audio (operating at stereo 44.1kHz) is also faster than
AudioLDM2-large and -music (operating at mono 16kHz)

Conclusions
Our latent diffusion model enables the rapid generation
of variable-length, long-form stereo music and sounds at
44.1kHz from textual and timing inputs. We explored novel
qualitative and quantitative metrics for evaluating long-form
full-band stereo signals, and found Stable Audio to be a top
contender, if not the top performer, in two public benchmarks. Differently from other state-of-the-art models, ours
can generate music with structure and stereo sound effects.


Moûsai (Schneider et al., 2023)
and AudioLDM (Liu et al., 2023a) pioneered using latent diffusion for text-to-music and -audio. Their main difference
being that Moûsai decodes latents onto waveforms through
a diffusion decoder, while AudioLDM decodes latents onto
spectrograms which are then inverted to waveforms with
HiFi-GAN (Kong et al., 2020). A

Modi:

Text-to-Audio:

Audio-to-Audio:

Input vocals: transform vocals into music and sound effects (beta)

Audio-to-audio
Learn how to add audio into your generations.

Pricing:

4 tiers: Free, Pro, Studio, Max

Free

It’s free.
Get started!
Monthly track generations
20
Track duration
Up to 3 minutes
Monthly upload amount
3 minutes
Cropped at 30 secs
License


Personal license

paid license give you the right to use the generated audio in commercial projects with below 100,000 MAU, commercial music releases, Social media, personal podcasts and videos.
For more MAU and Film, TV, advertising, games and apps, you need an Enterprise License.

Paid licenses give also more monthly track generations (pro: 500, Studio 1350, Max 4500).


User guides - well designed and nice to read.

Text to audio:

you describe the music you want to create in natural language, and the AI generates the music for you.  you give it musical descriptions based on genre, sub-genre, mood and instrument type.

you can create full instrumentals, individual stems, sound effects.

Examples:

Lofi hip hop beat, chillhop
Calm meditation music to play in a spa lobby

Manchmal auch eigenwillig:

Folk, live, atmospheric, soulful, acoustic guitar, smooth, soft

Schafft es aber in der weiteren Entwicklung etwas aufzulösen.


Individual stems:

Drums, Bass, 808 bass stabs
Drum solo

Auch: https://www.stableaudio.com/user-guide/prompt-structure

Effects:

...

Tipps: (Auch: https://www.stableaudio.com/user-guide/prompt-structure)

- add detail (the more detail the better)
- set the mood (musical: groovy, rhythmic, emotional: sad, happy, beautiful)
- chose instruments
- set the tempo (BPM or ...)



- also found: the loudness


Audio to audio:

- added to text
- you can use existing recordings, record on the fly, upload previous generations
- helps guide output goals
- timing, style transfer, vocal input to instrument output

https://www.stableaudio.com/user-guide/audio-to-audio

To protect creator copyrights, for audio uploads, we partner with Audible Magic to utilize their content recognition (ACR) technology to power real-time content matching to prevent copyright infringement.

Tolles interface. Einzigartiges Design, trotzdem intuitiv nutzbar. Nette Ideen, Slider Audio zu Text zum Beispiel. Auch tolle Doku - sehr kurz, strukturiert, viele Beispiele.

Extras: 

Steps:
Seed:
Prompt strength:

Keine API, keine Open Weights, aber Code zum Training und Inferenz sind Open Source.

Schönes Video: https://www.stableaudio.com/user-guide/model-2

Practical use:


I've used it to generate  background audio for this episode.

I find it fascinating to beatbox, whistle or sing an idea and have it transferred to a tune.

Overall I'm impressed by the quality of the resulting audio.

Stable Diffusion as a company has a chaling time, currently: The UK based AI company reportedly has only xxx revenue at xxx costs. It was not fully able to pay their cloud bills of ... and even have outstanding tax payments in the UK. XXX, the head of development for Stable Audio left the company after disagreements with the management whether training on copyrighted material can be considered fair use. This is an important topic for Stability AI as they already face lawsuits with Gettys for Stable Diffustion The current Stable Audio model was allegedly trained on xxx material, so users shouldn't worry about copyright claims. The former CXO resigned. I hope Stability AI can solve the issues and turn their business into a profitable one. They have been pivotal for the industry and very generous despite their comparatively small size.


Diffusion Model:

- forward: add noise eg. drawn from a normal distrbution to an image in a stochastic process (markov process).
- backward: remove noise
- an AI system learns the process
- traditionally UNet, now transformer
- the diffusion process is performed in many steps: smaller easier to learn, reversible (model can learn a sequence of reverse steps to reconstruct the original image from the noise), stable training, high quality generation of even complex images
- controlled noising, a fraction of the image information is retained, not completely random, not entirely uncorrelated with orig image..., this enables reversibility of the process
- markov chain: each step is only dependent on the previous step and not on the steps before that.
- the end of the forward process contains encoded information from the original image, but it's imperceptable by humans
- encoding is good enough that a correctly learned model can reconstruct the original image with remarkable accuracy and detail.

Transformers are used to model the sequence of denoising steps. They learn to predict the noise that was added at each step of the diffusion process and thus become able to reverse the process.

Normal transformer training: model is exposed to image - image pairs. Gradient descent is used to minimize the differences between predictions and the actual noise. The model becomes gradually better at prediction and thus reversing.


The transformer's capacity to model the denoising process is linked to the dimensionality of it's latent space. Higher dimensional latent space allows for more detailed representation of the denoising path, enabling the transformer to capture an replicate more complex patterns and structures inherent in the data.

?? As Stable Diffusion 3.0, there are independent transformers for each of the modalities (text and audio), but the model joins the sequences of the two for the attention operation. - MM-DiT (Multi Modal Diffusion Transformer)

Diffusion Transformer Architekture is also behind other multi modal transformers SORA, Stable Diffusion 3.0).

https://www.youtube.com/watch?v=XsB1frqzr9A