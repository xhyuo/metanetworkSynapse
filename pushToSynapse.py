import synapseclient
import argparse
import csv

def read_args():
    parser = argparse.ArgumentParser(description='push files to synapse')
    parser.add_argument('file', help='path to file to upload')
    parser.add_argument('parentId', help="Synapse ID of parent folder")
    parser.add_argument('annotationFile', help="Corresponding annotation file")
    parser.add_argument('provenanceFile', help="Corresponding provenance file")
    parser.add_argument('method', help="name of method used to generate file")
    args = parser.parse_args()
    return (args.file, args.parentId, args.annotationFile,
        args.provenanceFile, args.method)

def push(filePath, parentId, annotationFile, provenanceFile, method):
    syn = synapseclient.login()
    with open(annotationFile, 'r') as f:
        entries = f.read().strip().split('\n')
        annotations = {s[0] : s[1] for s in [pair.split(',') for pair in entries]}
        annotations['method'] = method
    with open(provenanceFile, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        used = [r['provenance'] for r in reader if r['executed'] == 'FALSE']
        executed= [r['provenance'] for r in reader if r['executed'] == 'TRUE']
    activity = synapseclient.Activity(name='Network Inference',
            description=method, used=used, executed=executed)
    synFile = synapseclient.File(filePath, parent=parentId)
    synEntity = syn.store(obj=synFile, activity=activity)
    syn.setAnnotations(synEntity, annotations)

def main():
    filePath, parentId, annotationFile, provenanceFile, method = read_args()
    push(filePath, parentId, annotationFile, provenanceFile, method)

if __name__ == "__main__":
    main()
