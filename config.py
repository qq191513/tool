def set_gpu():
    # 1������GPUģʽ
    session_config = tf.ConfigProto(
        device_count={'GPU': 0},
        gpu_options={'allow_growth': 1,
                     # 'per_process_gpu_memory_fraction': 0.1,
                     'visible_device_list': '0'},
        allow_soft_placement=True)
    return  session_config

def init_variables_and_start_thread(sess):
    # 2��ȫ�ֳ�ʼ�������������߳� ��Ҫ���ڳ�ʼ������֮��
    sess.run(tf.local_variables_initializer())
    sess.run(tf.global_variables_initializer())
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)


def restore_model(sess,ckpt):
    # 3���ָ�model�����������ȫ�ֳ�ʼ�������������̺߳���֮��
    """Set Saver."""
    var_to_save = [v for v in tf.global_variables(
    ) if 'Adam' not in v.name]  # Don't save redundant Adam beta/gamma
    saver = tf.train.Saver(var_list=var_to_save, max_to_keep=5)
    mode_file = tf.train.latest_checkpoint(ckpt)
    saver.restore(sess, mode_file)