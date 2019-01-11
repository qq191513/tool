def set_gpu():
    # 1、设置GPU模式
    session_config = tf.ConfigProto(
        device_count={'GPU': 0},
        gpu_options={'allow_growth': 1,
                     # 'per_process_gpu_memory_fraction': 0.1,
                     'visible_device_list': '0'},
        allow_soft_placement=True)
    return  session_config

def init_variables_and_start_thread(sess):
    # 2、全局初始化和启动数据线程 （要放在初始化网络之后）
    sess.run(tf.local_variables_initializer())
    sess.run(tf.global_variables_initializer())
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)


def restore_model(sess,ckpt):
    # 3、恢复model，放在上面的全局初始化和启动数据线程函数之后
    """Set Saver."""
    var_to_save = [v for v in tf.global_variables(
    ) if 'Adam' not in v.name]  # Don't save redundant Adam beta/gamma
    saver = tf.train.Saver(var_list=var_to_save, max_to_keep=5)
    mode_file = tf.train.latest_checkpoint(ckpt)
    saver.restore(sess, mode_file)

def stop_threads(coord,threads):
    # 4、程序终止 （该句要放到with graph和with sess 区域之内才行）
    coord.request_stop()
    coord.join(threads)