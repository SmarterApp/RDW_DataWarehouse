import csv
import os
import pystache
import argparse

schools = {
    "242": "Sunset - Eastern Elementary",
    "245": "Sunset - Western Middle",
    "248": "Sunset Central High",
    "939": "Daybreak - Western Middle",
    "942": "Daybreak Central High",
    "936": "Daybreak - Western Elementary",
    "9f033bff-7d5b-4800-8ad4-67f063b0ccd4": "Mountainash Serrano Jr Middle",
    "18283a0a-a139-4233-b8c0-f5c5aeea51d2": "Nyala Aurochs High School",
    "ccb4895f-0b6e-44dd-8b41-6293b0f5b3d4": "Serotine Planetree Elementary School",
    "0eab62f5-6c97-4302-abff-7bfdc61f527c": "Dolphin Razorfish Sch",
    "fbc3e9f6-ad16-4cf0-bb84-5f3fc6929b41": "Hickory Cornetfish Jr Middle",
    "1cc294ff-7b3f-4531-b9fc-9526138e4141": "Nunbird Manefish HS",
    "52a84cfa-4cc6-46db-8b59-5938fd1daf12": "Sandpiper Peccary Elementary",
    "e70e2681-ada0-4b21-9871-d747358297f0": "Kangaroo Hippopotamus Community Middle",
    "f7de5f75-b5ff-441a-9ed0-cd0e965f7719": "Serval Spearfish Middle",
    "fc85bac1-f471-4425-8848-c6cb28058614": "Gorilla Tapiti High School",
    "429804d2-50db-4e0e-aa94-96ed8a36d7d5": "Blobfish Pintail Sch"
}

districts = {
    "228": "Sunset School District",
    "228": "Sunset School District",
    "228": "Sunset School District",
    "229": "Daybreak School District",
    "229": "Daybreak School District",
    "229": "Daybreak School District",
    "2ce72d77-1de2-4137-a083-77935831b817": "Dealfish Pademelon SD",
    "2ce72d77-1de2-4137-a083-77935831b817": "Dealfish Pademelon SD",
    "2ce72d77-1de2-4137-a083-77935831b817": "Dealfish Pademelon SD",
    "2ce72d77-1de2-4137-a083-77935831b817": "Dealfish Pademelon SD",
    "0513ba44-e8ec-4186-9a0e-8481e9c16206": "Ropefish Lynx Public Schools",
    "0513ba44-e8ec-4186-9a0e-8481e9c16206": "Ropefish Lynx Public Schools",
    "0513ba44-e8ec-4186-9a0e-8481e9c16206": "Ropefish Lynx Public Schools",
    "0513ba44-e8ec-4186-9a0e-8481e9c16206": "Ropefish Lynx Public Schools",
    "c912df4b-acdf-40ac-9a91-f66aefac7851": "Swallow Harrier District",
    "c912df4b-acdf-40ac-9a91-f66aefac7851": "Swallow Harrier District",
    "c912df4b-acdf-40ac-9a91-f66aefac7851": "Swallow Harrier District"
}

# initialize parser
template = None

with open('template.xml') as f:
    template = f.read()


students = {}
asmt = {}


def prepare_student_data():
    with open('./data/dim_student.csv') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        for s in csv_reader:
            student_id = s[1]
            students[student_id] = s


def prepare_asmt_data():
    with open('./data/dim_asmt.csv') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        for a in csv_reader:
            asmt[a[0]] = {'name': a[7], 'effectiveDate': a[35]}


def convert(input_path, output_path, is_iab):
    prepare_student_data()
    prepare_asmt_data()
    with open(input_path) as f:
        csv_reader = csv.reader(f, delimiter=',')
        # first row contains header
        next(csv_reader)
        # convert each line to a TSB test file
        for l in csv_reader:
            asmt_rec_id, xml = convert_to_xml(l, is_iab)
            output_file = os.path.join(output_path, asmt_rec_id + ".xml")
            save(output_file, xml)


def save(output_file, content):
    print("writed file ", output_file)
    with open(output_file, "w") as o:
        o.write(content)


def convert_to_xml(l, is_iab):
    def _bool(value):
        if value == 'f':
            return "No"
        elif value == 't':
            return "Yes"
        else:
            return ""

    def _state_name(state_code):
        if state_code == 'ca':
            return 'California'
        elif state_code == 'nc':
            return 'North Carolina'
        return 'Hello World'

    def _date(date):
        if date == "":
            return ""
        return "{yyyy}-{mm}-{dd}T10:49:08.437".format(
            yyyy=date[0:4],
            mm=date[4:6],
            dd=date[6:8]
        )
    fact_asmt_index = {'demographics': 42,
                       'gender': 40,
                       'asmt': 24,
                       'acc': 54}
    fact_block_index = {'demographics': 26,
                        'gender': 24,
                        'asmt': 20,
                        'acc': 38}
    index = fact_asmt_index if not is_iab else fact_block_index
    data = {}
    data['subject'] = l[13].upper()
    data['asmt_year'] = l[12]
    data['asmt_type'] = l[11]
    data['grade'] = "%02d" % int(l[14])
    data['studentId'] = l[5]
    data['birthdate'] = _date(students[l[5]][6])
    data['firstName'] = students[l[5]][3]
    data['middleName'] = students[l[5]][4]
    data['lastName'] = students[l[5]][5]
    data['HispanicOrLatinoEthnicity'] = _bool(l[index['demographics']])
    data['AmericanIndianOrAlaskaNative'] = _bool(l[index['demographics'] + 1])
    data['Asian'] = _bool(l[index['demographics'] + 2])
    data['BlackOrAfricanAmerican'] = _bool(l[index['demographics'] + 3])
    data['NativeHawaiianOrOtherPacificIslander'] = _bool(l[index['demographics'] + 4])
    data['White'] = _bool(l[index['demographics'] + 5])
    data['DemographicRaceTwoOrMoreRaces'] = _bool(l[index['demographics'] + 6])
    data['sex'] = 'M' if l[index['gender']] == 'male' else 'F'
    data['GradeLevelWhenAssessed'] = "%02d" % int(l[15])
    # external ssid is empty in dim_student table, so I made it up here
    data['ExternalSSID'] = l[15]
    data['IDEAIndicator'] = _bool(l[index['demographics'] + 7])
    data['LEPStatus'] = _bool(l[index['demographics'] + 8])
    data['Section504Status'] = _bool(l[index['demographics'] + 9])
    data['EconomicDisadvantageStatus'] = _bool(l[index['demographics'] + 10])
    data['MigrantStatus'] = _bool(l[index['demographics'] + 11])
    data['DistrictID'] = l[7]
    data['DistrictName'] = districts[l[7]]
    data['SchoolID'] = l[8]
    data['SchoolName'] = schools[l[8]]
    data['StateCode'] = l[6].lower()
    data['effective_date'] = _date(asmt[l[1]]['effectiveDate'])
    data['clientName'] = _state_name(l[6])
    data['asmt_guid'] = l[4]
    data['oppId'] = l[9]
    data['where_taken_name'] = l[10]
    data['date_taken'] = _date(l[16])

    data['asmt_claim_1_score'] = l[index['asmt']]
    data['asmt_claim_1_score_range_min'] = l[index['asmt'] + 1]
    data['asmt_claim_1_score_range_max'] = l[index['asmt'] + 2 ]
    data['asmt_claim_1_perf_lvl'] = l[index['asmt'] + 3]

    data['is_iab'] = is_iab

    if not is_iab:
        data['asmt_perf_lvl'] = l[23]
        data['asmt_score'] = l[20]
        data['asmt_score_range_min'] = l[21]
        data['asmt_score_range_max'] = l[22]

        data['asmt_claim_2_score'] = l[28]
        data['asmt_claim_2_perf_lvl'] = l[31]
        data['asmt_claim_2_score_range_min'] = l[29]
        data['asmt_claim_2_score_range_max'] = l[30]

        data['asmt_claim_3_score'] = l[32]
        data['asmt_claim_3_perf_lvl'] = l[35]
        data['asmt_claim_3_score_range_min'] = l[33]
        data['asmt_claim_3_score_range_max'] = l[34]

        data['asmt_claim_4_score'] = l[36] or 0
        data['asmt_claim_4_perf_lvl'] = l[39] or 0
        data['asmt_claim_4_score_range_min'] = l[37] or 0
        data['asmt_claim_4_score_range_max'] = l[38] or 0
    else:
        data['iab_block_name'] = asmt[l[1]]['name']

    data['acc_asl_video_embed'] = l[index['acc']] or 0
    data['acc_noise_buffer_nonembed'] = l[index['acc'] + 1] or 0
    data['acc_print_on_demand_items_nonembed'] = l[index['acc'] + 2] or 0
    data['acc_braile_embed'] = l[index['acc'] + 3] or 0
    data['acc_closed_captioning_embed'] = l[index['acc'] + 4] or 0
    data['acc_text_to_speech_embed'] = l[index['acc'] + 5] or 0
    data['acc_abacus_nonembed'] = l[index['acc'] + 6] or 0
    data['acc_alternate_response_options_nonembed'] = l[index['acc'] + 7] or 0
    data['acc_calculator_nonembed'] = l[index['acc'] + 8] or 0
    data['acc_multiplication_table_nonembed'] = l[index['acc'] + 9] or 0
    data['acc_print_on_demand_nonembed'] = l[index['acc'] + 10] or 0
    data['acc_read_aloud_nonembed'] = l[index['acc'] + 11] or 0
    data['acc_scribe_nonembed'] = l[index['acc'] + 12] or 0
    data['acc_speech_to_text_nonembed'] = l[index['acc'] + 13] or 0
    data['acc_streamline_mode'] = l[index['acc'] + 14] or 0

    xml = pystache.render(template, data)
    return l[0], xml


def main():
    parser = argparse.ArgumentParser(description='Convert CSV files to TSB XML files for E2E testing')
    parser.add_argument('-i', '--input', default="./data/fact_asmt_outcome_vw.csv", help='path to CSV files')
    parser.add_argument('-o', '--output', default="./output", help='path to output directory')
    parser.add_argument('-b', '--block', action='store_true', help='Input file is an Interim Assessment Block File')
    args = parser.parse_args()

    convert(args.input, args.output, args.block)

if __name__ == '__main__':
    main()
