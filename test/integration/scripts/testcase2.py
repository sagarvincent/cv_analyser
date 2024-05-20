from backend.parsing_fun import cv_parse
from backend.similarity_score import similarity_score


def testcase1(cv_path,jd_path):


    try:
        with open(jd_path,'r') as file:
            jd = file.read()
    except:
        print("JD couldn't be loaded.")
    parser = cv_parse()
    parsed_data = parser.parse_cv_file(cv_path)
    s = similarity_score(parsed_data, jd)
    cv_score, score_explanation = s.sim_score()


    return cv_score, score_explanation




if __name__=="__main__":

    cv_path = "test\integration\data\testcase2_cv.pdf" 
    jd_path = "test\integration\data\testcase_jd.txt"

    cv_score, score_explanation = testcase1(cv_path,jd_path)