cd ./diameterTables/

for FILE in *
do
    cp -R ../bmdc ../exampleCase/system/blockMeshDict
    python3 ../pythonScripts/blockMeshgen.py <<ENDOF
./${FILE}
ENDOF
    key=$(python3 ../pythonScripts/keygen.py)    
    rm -rf ../patientCases/${key}${FILE}
    cp -R ../exampleCase/ ../patientCases/${key}${FILE}
    mv ${FILE} ${key}${FILE}
    cd ../patientCases/${key}${FILE}/
    blockMesh >bmlog
    cd -
done
