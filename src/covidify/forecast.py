#___________________ ________________________________________________________
class Wrap:
    '''Resource-intensive object'''
    def P_Wrap(self):
        print("creating report folder")
class WrapProxy:
    '''Relatively less resource-intensive proxy acting as middleman.
     Instantiates a College object only if there is no fee due.'''
    def __init__(self,path):
        path="true"
    def isPathEstablished(self):
        print("Proxy in action. Checking to see if the path exists or not...")
        if not os.path.exists(image_dir):
            print('Creating reports folder...')
            os.system('mkdir -p ' + image_dir)
        else:
            print("path established")  
WrapProxy=WrapProxy()
wrapProxy.isPathEstablished(os.path.exists(image_dir))
