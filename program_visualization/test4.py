
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config
from pycallgraph import GlobbingFilter
import cv2
##############################    改这里      ####################################

# from test5 import */
from logistic_regression import logistic
#希望包含的函数
# myinclude = [
#     'main',
#     'Activation',
#     'MaxPooling2D',
#     'Convolution2D'
# ]
def main():
    # 你的主函数代码。
    # download('http://www.baidu.com/img/bd_logo1.png', r'./fuck.png')
    logistic()
###############################   end      #######################################

if __name__ == "__main__":
    config = Config()
    # 关系图中包括(include)哪些函数名。
    # 如果是某一类的函数，例如类gobang，则可以直接写'gobang.*'，表示以gobang.开头的所有函数。（利用正则表达式）。
    # config.trace_filter = GlobbingFilter(include=myinclude)
    # 该段作用是关系图中不包括(exclude)哪些函数。(正则表达式规则)
    config.trace_filter = GlobbingFilter(exclude=[
        'pycallgraph.*',
        '*.secret_function',
        'FileFinder.*',
        'ModuleLockManager.*',
        'SourceFilLoader.*'
    ])
    # config.trace_filter = GlobbingFilter(include=myinclude)
    graphviz = GraphvizOutput()
    save_name = 'graph.png'
    graphviz.output_file = save_name
    with PyCallGraph(output=graphviz, config=config):
    # with PyCallGraph(output=graphviz):
        main()
    mat = cv2.imread(save_name)
    cv2.imshow(save_name,mat)
    cv2.waitKey(10000)