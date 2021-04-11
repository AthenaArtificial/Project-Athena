########################
######  AthenaAI  ######
######    2021    ######
########################

import gpt_2_simple as gpt2

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)

question_to_ask = ""  # Put question here (as short as possible) and test the result.

answer = gpt2.generate(sess, length=100, include_prefix=True, temperature=0.1, top_k=1, top_p=0.9, run_name='run1', prefix=question_to_ask, return_as_list=True)[0]

print(answer)