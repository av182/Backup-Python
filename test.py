import	os, sys
import shutil

dirpath=r'D:\distr\zwc\ecl'
dstpath=r'D:\PY\backup\21012016-135618_full'
fl='tetsetsaetawetatargagagatetsetsaetawetatargagagatetsetsaetawetatargagagatetsetsaetawetatargagagatetsetsaetawetatargagagatetsetsaetawetatargagagatetsetsaetawetatargagagatetsetsaetawetatargagagatetsetsaetawetatargagagatetsetsaetawetatargaga.txt'
fullsrcpath = os.path.join(dirpath, fl)
fulldstpath = os.path.join(dstpath, fl)
print(len(fl)+len(dirpath))
print(len(fl)+len(dstpath))
#shutil.copy2(fullsrcpath, fulldstpath)
