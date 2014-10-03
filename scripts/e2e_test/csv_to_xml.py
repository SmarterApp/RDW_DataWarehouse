import csv
import os
import pystache
import argparse


effective_date_mapping = {
    "1000000020": "20160404",
    "1000000021": "20160404",
    "1000000022": "20150404",
    "1000000023": "20150404",
    "1000000024": "20150404",
    "1000000025": "20150404",
    "1000000026": "20160404",
    "1000000027": "20160404",
    "1000000028": "20150404",
    "1000000029": "20150404",
    "1000000030": "20150404",
    "1000000031": "20150404",
    "1000000032": "20150404",
    "1000000033": "20150404",
    "1000000034": "20150404",
    "1000000035": "20140902",
    "1000000036": "20150902",
    "1000000037": "20140902",
    "1000000038": "20160106",
    "1000000039": "20150106",
    "1000000040": "20150106",
    "1000000041": "20160106",
    "1000000042": "20140902",
    "1000000043": "20150902",
    "1000000044": "20150902",
    "1000000045": "20160106",
    "1000000046": "20150106",
    "1000000047": "20150106",
    "1000000048": "20160106",
    "1000000049": "20140902",
    "1000000050": "20150902"
}

# initialize parser
template = None

with open('template.xml') as f:
    template = f.read()


def convert(input_path, output_path):
    with open(input_path) as f:
        csv_reader = csv.reader(f, delimiter=',')
        # first row contains header
        next(csv_reader)
        # convert each line to a TSB test file
        for l in csv_reader:
            asmt_rec_id, xml = convert_to_xml(l)
            output_file = os.path.join(output_path, asmt_rec_id + ".xml")
            save(output_file, xml)


def save(output_file, content):
    print("writed file ", output_file)
    with open(output_file, "w") as o:
        o.write(content)


def convert_to_xml(l):

    def _bool(value):
        if value == 'f':
            return "No"
        elif value == 't':
            return "Yes"
        else:
            return ""

    def _state_name(state_code):
        if state_code == 'CA':
            return 'California'
        elif state_code == 'NC':
            return 'North Carolina'
        return 'Hello World'

    def _date(date):
        if date == "":
            return ""
        return "{yyyy}-{mm}-{dd}T11:13:40.900".format(
            yyyy=date[0:4],
            mm=date[4:6],
            dd=date[6:8]
        )

    data = {}
    data['subject'] = l[13].upper()
    data['asmt_year'] = l[12]
    data['asmt_type'] = l[11]
    data['grade'] = l[14]
    data['studentId'] = l[5]
    data['HispanicOrLatinoEthnicity'] = _bool(l[42])
    data['AmericanIndianOrAlaskaNative'] = _bool(l[43])
    data['Asian'] = _bool(l[44])
    data['BlackOrAfricanAmerican'] = _bool(l[45])
    data['NativeHawaiianOrOtherPacificIslander'] = _bool(l[46])
    data['White'] = _bool(l[47])
    data['DemographicRaceTwoOrMoreRaces'] = _bool(l[48])
    data['sex'] = 'M' if l[40] == 'male' else 'F'
    data['GradeLevelWhenAssessed'] = l[15]
    # external ssid is empty in dim_student table, so I made it up here
    data['ExternalSSID'] = l[15]
    data['IDEAIndicator'] = _bool(l[49])
    data['LEPStatus'] = _bool(l[50])
    data['Section504Status'] = _bool(l[51])
    data['EconomicDisadvantageStatus'] = _bool(l[52])
    data['MigrantStatus'] = _bool(l[53])
    data['DistrictID'] = l[7]
    data['SchoolID'] = l[8]
    data['StateCode'] = l[6]
    data['effective_date'] = _date(effective_date_mapping.get(l[1]))
    data['clientName'] = _state_name(l[6])
    data['asmt_guid'] = l[4]
    data['oppId'] = l[9]
    data['where_taken_name'] = l[10]
    data['date_taken'] = _date(l[16])

    data['asmt_score'] = l[20]
    data['asmt_score_range_min'] = l[21]
    data['asmt_score_range_max'] = l[22]
    data['asmt_perf_lvl'] = l[23]

    data['asmt_claim_1_score'] = l[24]
    data['asmt_claim_1_perf_lvl'] = l[27]
    data['asmt_claim_1_score_range_min'] = l[25]
    data['asmt_claim_1_score_range_max'] = l[26]

    data['asmt_claim_2_score'] = l[28]
    data['asmt_claim_2_perf_lvl'] = l[31]
    data['asmt_claim_2_score_range_min'] = l[29]
    data['asmt_claim_2_score_range_max'] = l[30]

    data['asmt_claim_3_score'] = l[32]
    data['asmt_claim_3_perf_lvl'] = l[35]
    data['asmt_claim_3_score_range_min'] = l[33]
    data['asmt_claim_3_score_range_max'] = l[34]

    data['asmt_claim_4_score'] = l[36]
    data['asmt_claim_4_perf_lvl'] = l[39]
    data['asmt_claim_4_score_range_min'] = l[37]
    data['asmt_claim_4_score_range_max'] = l[38]

    data['acc_asl_video_embed'] = l[54]
    data['acc_noise_buffer_nonembed'] = l[55]
    data['acc_print_on_demand_items_nonembed'] = l[56]
    data['acc_braile_embed'] = l[57]
    data['acc_closed_captioning_embed'] = l[58]
    data['acc_text_to_speech_embed'] = l[59]
    data['acc_abacus_nonembed'] = l[60]
    data['acc_alternate_response_options_nonembed'] = l[61]
    data['acc_calculator_nonembed'] = l[62]
    data['acc_multiplication_table_nonembed'] = l[63]
    data['acc_print_on_demand_nonembed'] = l[64]
    data['acc_read_aloud_nonembed'] = l[65]
    data['acc_scribe_nonembed'] = l[66]
    data['acc_speech_to_text_nonembed'] = l[67]
    data['acc_streamline_mode'] = l[68]

    xml = pystache.render(template, data)
    return l[0], xml


def main():
    parser = argparse.ArgumentParser(description='Convert CSV files to TSB XML files for E2E testing')
    parser.add_argument('-i', '--input', default="./data/fact_asmt_outcome_vw.csv", help='path to CSV files')
    parser.add_argument('-o', '--output', default="./output", help='path to output directory')
    args = parser.parse_args()

    convert(args.input, args.output)

if __name__ == '__main__':
    main()
