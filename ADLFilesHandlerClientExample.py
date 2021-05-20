import ADLFilesHandler, yaml

with open('ADLFilesHandlerYAMLExample.yaml', 'r') as file:
    YAMLConfig = yaml.load(file, Loader=yaml.FullLoader)

adlfh = ADLFilesHandler.ADLFilesHandler(YAMLConfig)
adlfh.run()
