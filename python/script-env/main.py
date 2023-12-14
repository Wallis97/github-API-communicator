#!/usr/bin/python3
import argparse
import os
import requests
import json
# import xmltodict

def main():

    URL = "gitlab.com/api/v4"
    # this is security issue for sure :)
    personalAccessToken = os.getenv("GITLAB_TOKEN")


    parser = argparse.ArgumentParser(
        prog='GitLab API Script',
        description='A simple script for retrieving information about GitLab projects via GitLab API')
    


    ## Define scripts arguments   
    parser.add_argument('projectID', type=ascii,
                        help="specify project by providing its ID")

    parser.add_argument('-p','--pipelines', required=False, action="store_true",
                        help="info about projects pipelines")
    
    parser.add_argument('-b','--branch', required=False, action="store_true",
                        help="info about projects branches")
    
    parser.add_argument('-c','--commit', required=False, action="store_true",
                        help="info about projects commits")
    
    parser.add_argument('-t','--tag', required=False, action="store_true",
                        help="info about projects tags")
    
    parser.add_argument('-j','--job', required=False, action="store_true",
                        help="info about projects jobs")
    
    parser.add_argument('-m','--merge_request', required=False, action="store_true",
                        help="info about projects merge requests")
    
    # I really don't want to program this option,
    # Maybe in the future I'll find some motivation to do this 
    # parser.add_argument('-o','--output', choices=['json','yaml', 'xml'], default='json', nargs='?',
    #                     help="specify output format (JSON by default)")

    args = parser.parse_args()

    pipelineData =''
    branchData =''
    commitData =''
    tagData =''
    jobData =''
    mergeRequestData =''

    # for some reason terminal adds quotas to the input
    projectID = args.projectID[1:-1]


    ## Logic for provided parameters
    print(f"https://{URL}/projects/{projectID}/pipelines/?private_token={personalAccessToken}")
    if args.pipelines:
        r = requests.get(f"https://{URL}/projects/{projectID}/pipelines/?private_token={personalAccessToken}")
        if r.status_code == 200:
            pipelineData = '{"pipeline_data":' + r.text + '}'
    if args.branch:
        r = requests.get(f"https://{URL}/projects/{projectID}/repository/branches/?private_token={personalAccessToken}")
        if r.status_code == 200:
            branchData = '{"branches_data":' + r.text + '}'
    if args.commit:
        r = requests.get(f"https://{URL}/projects/{projectID}/repository/commits/?private_token={personalAccessToken}")
        if r.status_code == 200:
            commitData = '{"branches_data":' + r.text + '}'
    if args.tag:
        r = requests.get(f"https://{URL}/projects/{projectID}/repository/tags/?private_token={personalAccessToken}")
        if r.status_code == 200:
            tagData = '{"branches_data":' + r.text + '}'
    if args.job:
        r = requests.get(f"https://{URL}/projects/{projectID}/jobs/?private_token={personalAccessToken}")
        if r.status_code == 200:
            jobData = '{"branches_data":' + r.text + '}'
    if args.merge_request:
        r = requests.get(f"https://{URL}/projects/{projectID}/merge_requests/?private_token={personalAccessToken}")
        if r.status_code == 200:
            mergeRequestData = '{"branches_data":' + r.text + '}'
    

    output = ''

    # append data from respective arguments to the output
    if pipelineData != '':
        output += pipelineData + ','
    if branchData != '':
        output += branchData + ','
    if commitData != '':
        output += commitData + ','
    if tagData != '':
        output += tagData + ','
    if jobData != '':
        output += jobData + ','
    if mergeRequestData != '':
        output += mergeRequestData

    # remove a comma from the end of the string 
    if output[-1] == ',':
        output = output[0:-1]
    
    
    json_data = json.loads('['+output+']')

    # if args.output is not None:
    #     match args.output:
    #         case 'yaml':
    #             output = json.dumps(json_data, indent=2)
    #         case 'xml':
    #             output = xmltodict.unparse(json_data)

    output = json.dumps(json_data, indent=2)
    print(output)
    return output


if __name__== "__main__":
    main()