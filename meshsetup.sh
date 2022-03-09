cd ./diameterTables/

for FILE in *
do
    cp -R ../bmdc ../exampleCase/system/blockMeshDict
    python3 ../pythonScripts/blockMeshgen.py <<ENDOF
./${FILE}
ENDOF
    key=$(python3 ../pythonScripts/keygen.py)    
    rm -rf ../patientCases/${FILE:0:7}${key}
    cp -R ../exampleCase/ ../patientCases/${FILE:0:7}${key}
    mv ${FILE} ${FILE:0:7}${key}.csv
    cd ../patientCases/${FILE:0:7}${key}/
    blockMesh >bmlog
    cd -
done
