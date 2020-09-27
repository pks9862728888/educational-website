def _validate_video_file(self, file):
    """Checking whether the file is video file"""
    try:
        if not file:
            return Response({'error': _('File is required.')},
                            status=status.HTTP_400_BAD_REQUEST)
        elif not filetype.is_video(file):
            return Response({'error': _('Not a valid video file.')},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'error': _('Error occurred.')},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)





if request.data.get('content_type') == models.StudyMaterialContentType.VIDEO:
    validate = self._validate_video_file(request.data.get('file'))

    if validate:
        models.InstituteSubjectCourseContent.objects.filter(
            pk=course_content_serializer.data['id']).first().delete()
        return validate

    video_serializer = serializer.VideoStudyMaterialSerializer(
        data={
            'video_study_material': course_content_serializer.data['id'],
            'file': request.data.get('file'),
            'can_download': request.data.get('can_download')
        }, context={"request": request})

    if video_serializer.is_valid():
        video_serializer.save()
        subject_stats.storage += size
        subject_stats.save()
        institute_stats.storage += size
        institute_stats.save()

        # Creating steamable files
        file_obj = models.SubjectVideoStudyMaterial.objects.filter(
            pk=video_serializer.data['id']).first()

        try:
            video_file_path = MEDIA_ROOT + '/' + str(file_obj.file)
            video = ffmpeg_streaming.input(video_file_path)

            ffprobe = FFProbe(video_file_path)
            video_format = ffprobe.format()
            duration = video_format['duration']
            bit_rate = video_format['bit_rate']
            print(ffprobe.video_size)

            _144p = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
            _240p = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
            _360p = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
            _480p = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
            _720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
            abs_file_path = models.hls_encoded_video_saving_file_name_path(str(file_obj.file))
            rel_file_path = abs_file_path.replace(MEDIA_ROOT, '').strip('//')
            hls_key_saving_abs_path = (models.hls_key_saving_path(str(file_obj.file)))
            hls_key_saving_rel_path = hls_key_saving_abs_path.replace(MEDIA_ROOT, '').strip('//')
            url = self.request.build_absolute_uri('/').strip("/") + MEDIA_URL + hls_key_saving_rel_path

            hls = video.hls(Formats.h264())
            # , _240p, _360p, _480p, _720p
            hls.representations(_144p)
            hls.encryption(hls_key_saving_abs_path, url, 5)
            hls.output(abs_file_path, monitor=monitor)

            file_obj.duration = Decimal(duration)
            file_obj.bit_rate = bit_rate
            file_obj.stream_file = rel_file_path
            file_obj.save()

            response['data'] = get_video_study_material_data(
                file_obj,
                'OBJ',
                self.request.build_absolute_uri('/').strip("/") + MEDIA_URL
            )
        except Exception:
            file_obj.error_transcoding = True
            file_obj.save()
            raise Exception()

        return Response(response, status=status.HTTP_201_CREATED)