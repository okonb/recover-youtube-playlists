#!/bin/bash

if [ "$1" = "--no-remove" ]
then
    NO_REMOVE="y"
fi

echo Testing for lxml...

if ! `pip show lxml 2>/dev/null 1>/dev/null`
then
    echo "No lxml, proceeding without"
    NO_LXML_OPTION="--no-lxml";
else
    echo "Found lxml"
fi

print_testcase (){
    echo -n \[TEST] extractor: $1 testfile: $2 output format: $3...
}

TESTFILES_DIR=./testfiles/;
TEST_OUTPUT_ROOT_DIR="./output/"

EXPECTED_SUBDIR="/expected/"

to_remove=""

exit_code=0;

mkdir -p output;

echo Running tests

for extractor_version in `ls $TESTFILES_DIR | grep v[0-9+]`
do
    current_extractor_path="$TESTFILES_DIR/$extractor_version"
    for testfile in `ls $current_extractor_path | grep testfile_[0-9+]\.html`
    do
        stripped_testfile="${testfile%.*}"
        current_input_path=$current_extractor_path/$testfile
        for fileformat in csv excel-csv json
        do
            current_extra_filename="out_${stripped_testfile}_${extractor_version}_extra.json"
            current_output_filename="out_${stripped_testfile}_${extractor_version}.${fileformat}"
            current_output_path="${TEST_OUTPUT_ROOT_DIR}/${current_output_filename}"
            current_expected_path=$current_extractor_path/expected/$current_output_filename
            current_expected_extra_path=$current_extractor_path/expected/$current_extra_filename
            current_test_command="
                python3 ../recover_playlist.py ${current_input_path} \
                    --extractor ${extractor_version} --extra-info ${NO_LXML_OPTION} \
                    -o ${current_output_path} --format ${fileformat} --write-info
            "

            print_testcase $extractor_version $stripped_testfile $fileformat

            eval $current_test_command 1>/dev/null # 2>/dev/null   # uncomment if you feel like it
            
            if test $? -ne 0
            then
                echo -e "\t\t[FAILED]"
                echo "executed command:"
                echo $current_test_command
                echo ""
                exit_code=1
                continue
            fi

            if ! `diff $current_output_path $current_expected_path`
            then
                echo -e "\t\t[FAILED]"
                echo "executed command:"
                echo $current_test_command
                echo "Produced file doesn't match the expected one:"
                echo $current_expected_path
                echo ""
                exit_code=1
                continue
            fi

            if ! `diff extra.json $current_expected_extra_path`
            then
                echo -e "\t\t[FAILED]"
                echo "executed command:"
                echo $current_test_command
                echo "Produced extra info file doesn't match the expected one:"
                echo $current_expected_extra_path
                echo ""
                exit_code=1
                continue
            fi

            to_remove="${current_output_path} ${to_remove}"
            echo -e "\t\t[PASSED]"
        done
    done
done

if test $exit_code -ne 0
then
    echo "Output files for failed tests can be found in ./output"
else
    echo "All tests completed successfully"
fi

if test -z "$NO_REMOVE"
then
    rm -f $to_remove extra.json
fi

exit $exit_code