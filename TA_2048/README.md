# Final Project: Explorations in 2048

My friend Thomas and I explored the game of 2048 through reinforcement learning for our final project. We primarily looked at [this paper](https://arxiv.org/pdf/2212.11087) which had a lot of findings related to 2048.

Most of this code is exploratory, and so not the most documented. Our findings are documented below though.

I was going to rewrite the entire explanation, but it would be easier to point you to [our slides](https://docs.google.com/presentation/d/1nqJiLR1CccifZeUgo5CfAm-6XsqgT-WM18cNRTvcPoc/edit?usp=sharing). They are not super-detailed, but should give you a general idea of our findings. Also, at some point afterwards, I was inspired by [this youtube video](https://www.youtube.com/watch?v=YGLNyHd2w10) to try and visualize the 2048 2x2 state space (and later, 4x4) in 3d. I have a rudimentary viewer in [this file](state_space_2x2_3d_viewer.py), and I am actively working on improving it. 

Some of the code is in this repo. Not all of it, simply because some files (for example, the model files) were too big to include.

Ultimately, because of our limited computer resources and the short timescale of this project, while we were able to get a model working better than a random player (about 2x the average score), we could not get one working as good as the one from the paper given. This makes sense, they put more resources into making a model for the game.

Ultimately, we created (partly vibecoded) [a website](http://www.aayanarish.com/ml_2048/) that allows you to both try playing 2048 yourself, but also see the model's suggested moves, and watch the model auto-play by itself. The model mentioned is the one from the paper, not ours, because ours was quite bad and wouldn't make for a good demonstration. I do want to clarify though, we are not taking any credit for the model that we demonstrated. Through the slides and appropriate conversations with our teacher, we demonstrated understanding of their approach, but were not able to replicate their results in the time (and given the computing restraints) we had. With more time, it would have been ideal to have a model of our own working nearly as well as theirs.