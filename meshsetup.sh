cd ./diameterTables/

for FILE in *
do
    cp -R ../bmdc ../exampleCase/system/blockMeshDict
    python3 ../pythonScripts/blockMeshgen.py <<ENDOF
./${FILE}
ENDOF
    rm -rf ../patientCases/P${FILE:0:7}case
    cp -R ../exampleCase/ ../patientCases/P${FILE:0:7}case
    cd ../patientCases/P${FILE:0:7}case/
    blockMesh >bmlog
    cd -
done
