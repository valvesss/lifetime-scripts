class ADLFilesHandler(object):
    def __init__(self, YAMLConfig):
        self.srcDstParquet = {}
        self.dstPathFiles = []
        self.YAMLConfig = YAMLConfig
        self.sourceRootPath = YAMLConfig['sourceRootPath']
        self.destinyRootPath = YAMLConfig['destinyRootPath']
        self.excludeEntries = ['adlPrdPath', 'sourceRootPath', 'destinyRootPath']

    def startSession(self):
        adl_path = self.YAMLConfig['adlPrdPath']
        connection_id = 'azure_data_lake_default'
        # Use your connection method
        self.adl, _ = ADLHook(adl_path, connection_id).get_client()

    def sourceYAMLIterator(self):
        for entry in self.YAMLConfig:
            if entry not in self.excludeEntries:
                for parquetPath in self.YAMLConfig[entry].values():
                    self.extractFilepaths(parquetPath)
                    self.createDestinyDir(parquetPath)

    def extractFilepaths(self, parquetPath):
        sourceParquetPath = self.sourceRootPath + parquetPath
        destinyParquetPath = self.destinyRootPath + parquetPath
        self.srcDstParquet[sourceParquetPath] = destinyParquetPath

    def createDestinyDir(self, parquetPath):
        # Split nested dirs in path
        parquetPathSplitted = parquetPath.split('/')
        # Removes empty entries
        parquetPathSplittedFiltered = list(filter(None, parquetPathSplitted))
        dstPathfile = self.destinyRootPath
        # Append each dir name to destiny name to create (nested or not) destiny dir
        # and exclude .parquet name file by not iterating through last name in list
        for i in range(len(parquetPathSplittedFiltered)-1):
            dstPathfile += parquetPathSplittedFiltered[i] + '/'
            # Check if destiny dir wasn't appended/created previously at this runtime
            if dstPathfile not in self.dstPathFiles:
                self.dstPathFiles.append(dstPathfile)
                self.adl.mkdir(dstPathfile)

    def moveFiles(self):
        for source, destiny in self.srcDstParquet.items():
            self.adl.mv(source, destiny)

    def run(self):
        self.startSession()
        self.sourceYAMLIterator()
        self.moveFiles()
