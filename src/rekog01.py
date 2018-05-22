import boto3
import sys

if __name__ == "__main__":

    group_photo_bucket=''
    reference_photo_bucket=''
    sourceFile=''
    targetFile=''
    s3 = boto3.resource('s3')
    s3_2 = boto3.resource('s3')
    b_ref = s3.Bucket(reference_photo_bucket)
    b_group = s3_2.Bucket(group_photo_bucket)
    client=boto3.client('rekognition','us-east-1')

    for group_obj in b_group.objects.all():
        for ref_obj in b_ref.objects.all():
            #print "ref: {0} {1}".format(ref_obj.bucket_name, ref_obj.key)
            #print "group: {0} {1}".format(group_obj.bucket_name, group_obj.key)
            sys.stdout.write('.')
            sys.stdout.flush()
            try:
                response=client.compare_faces(SimilarityThreshold=70,
                                SourceImage={'S3Object':{'Bucket':ref_obj.bucket_name,'Name':ref_obj.key}},
                                TargetImage={'S3Object':{'Bucket':group_obj.bucket_name,'Name':group_obj.key}})
            except client.exceptions.InvalidParameterException as e:
                print e
                print "ref: {0} {1}, group: {2} {3}".format(ref_obj.bucket_name, ref_obj.key,group_obj.bucket_name, group_obj.key)
            except client.exceptions.InvalidImageFormatException as e:
                print e
                print "ref: {0} {1}, group: {2} {3}".format(ref_obj.bucket_name, ref_obj.key,group_obj.bucket_name, group_obj.key)

            for faceMatch in response['FaceMatches']:
                print "\nFound a match: ref: {0} {1}, group: {2} {3}".format(ref_obj.bucket_name, ref_obj.key,group_obj.bucket_name, group_obj.key)
                position = faceMatch['Face']['BoundingBox']
                confidence = str(faceMatch['Face']['Confidence'])
                print('The face at ' +
                    str(position['Left']) + ' ' +
                    str(position['Top']) +
                    ' matches with ' + confidence + '% confidence')

