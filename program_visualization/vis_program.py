
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config
from pycallgraph import GlobbingFilter
import cv2
import os
##############################    改这里      ####################################
myinclude = [
'train_app.*',
'train_mars.*',
'vis_tools.*',
'queued_trainer.*',
'metrics.*',
'losses.*',
'network_definition.*',
'residual_net.*',
'mars.*',
'util.*',
]
def vis_program():
    # 这里写要观察的主函数代码。
    from train_mars import main_fuck
    main_fuck()
#希望包含的函数

###############################   end      #######################################

if __name__ == "__main__":
    config = Config()
    # 关系图中包括(include)哪些函数名。
    # 如果是某一类的函数，例如类gobang，则可以直接写'gobang.*'，表示以gobang.开头的所有函数。（利用正则表达式）。
    # config.trace_filter = GlobbingFilter(include=myinclude),
    # 该段作用是关系图中不包括(exclude)哪些函数。(正则表达式规则)
    #################   排除过滤     ########################
    # config.trace_filter = GlobbingFilter(exclude=[
    #     'pycallgraph.*',
    #     '*.secret_function',
    #     'FileFinder.*',
    #     '_ModuleLockManager.*',
    #     'SourceFilLoader.*',
    # ],
    # include=myinclude)
    #################   end     ###########################

    #################   包含过滤     ########################
    config.trace_filter = GlobbingFilter(include=myinclude)
    #################   end     ###########################

    graphviz = GraphvizOutput()
    save_name = 'graph.png'
    graphviz.output_file = save_name
    with PyCallGraph(output=graphviz, config=config):
    # with PyCallGraph(output=graphviz):
        vis_program()
    # mat = cv2.imread(save_name)
    # cv2.imshow(save_name,mat)
    # cv2.waitKey(10000)
    #显示图片，不用cv2
    command = 'eog '+save_name
    str = os.system('%s' % (command))