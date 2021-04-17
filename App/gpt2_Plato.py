import gpt_2_simple as gpt2


sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, checkpoint_dir="Plato/checkpoint")
answer = gpt2.generate(sess, length=100, include_prefix=False, temperature=0.1, top_k=1, top_p=0.9,
                       model_dir="Plato/models", sample_dir="Plato/samples", checkpoint_dir="Plato/checkpoint",
                       run_name='run1', prefix="What is philosophy", return_as_list=True)

print(answer[0])