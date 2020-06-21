import { ApiService } from './../../../api.service';
import { Component, OnInit, Type, } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';
import { ImageCroppedEvent, base64ToFile } from 'ngx-image-cropper';
import { HttpEventType } from '@angular/common/http';

interface ImageUploadResponse {
  type: number;
  loaded: number;
  total: number;
  body: {
    id: string;
    image: string;
    class_profile_picture: boolean;
    public_profile_picture: boolean;
    uploaded_on: string;
  };
  headers: {
    ok: boolean;
    status: number;
    statusText: string;
    type: number;
    url: string;
  };
}

@Component({
  selector: 'app-upload-profile-picture',
  templateUrl: './upload-profile-picture.component.html',
  styleUrls: ['./upload-profile-picture.component.css']
})
export class UploadProfilePictureComponent implements OnInit {

  // For detecting whether device is mobile
  mobileQuery: MediaQueryList;

  // For showing the chosen file & error
  chosenFile: string;
  imageError: string;

  // ImageCropperSettings
  rotation = 0;

  // For storing the image file
  croppedImage: any = '';
  profilePictureToUpload: File;
  fileNotChosen = true;
  choosePictureTarget: string;

  // Form control data
  classProfilePicture = true;
  publicProfilePicture = false;

  // For showing the upload progress
  showIndeterminateProgress = false;
  uploadProgress: number;

  // For sending status whether file is uploaded successfully or not
  pictureSuccessfullyUploaded = {
    status: false,
    classProfilePictureChanged: false
  };

  // For cropping image to visible ratio
  imageChangedEvent: any = '';

  constructor( private media: MediaMatcher,
               private apiService: ApiService) {
    this.mobileQuery = media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {}

  onProfilePictureSelected(event) {
    // Checking whether the image file is valid or not
    const filename = event.target.files[0].name.toLowerCase().split('.');
    const extension = filename[filename.length - 1];
    const regex = new RegExp('^(jpeg|png|jpg|webp)$');
    if (regex.test(extension)) {
      // Checking whether the image file size is not empty file
      if (event.target.files[0].size !== 0 ) {
        this.chosenFile = event.target.files[0].name;
        this.imageChangedEvent = event;
        this.fileNotChosen = false;
        this.imageError = null;
      } else {
        this.chosenFile = null;
        this.fileNotChosen = true;
        this.imageChangedEvent = null;
        this.imageError = 'Choose a valid image';
      }
    } else {
      this.chosenFile = null;
      this.fileNotChosen = true;
      this.imageChangedEvent = null;
      this.imageError = 'Invalid image';
    }
  }

  // This function will be called every time image is resized
  imageCropped(event: ImageCroppedEvent) {
    // After cropping
    this.croppedImage = event.base64;
    const blobFile = base64ToFile(this.croppedImage);

    // Before cropping
    const originalImage = this.imageChangedEvent.target.files[0];

    // Preparing the file to upload
    this.profilePictureToUpload = new File([blobFile], originalImage.name, {type: originalImage.type});
  }

  uploadProfilePicture() {
    if (this.classProfilePicture || this.publicProfilePicture) {
      this.showIndeterminateProgress = true;
      this.choosePictureTarget = '';
      const data = {
        profilePictureToUpload: this.profilePictureToUpload,
        class_profile_picture: this.classProfilePicture,
        public_profile_picture: this.publicProfilePicture
      };

      this.apiService.uploadProfilePicture(data).subscribe(
        (events: ImageUploadResponse) => {
          if (events.type === HttpEventType.UploadProgress) {
            // Showing progress in progress bar
            this.showIndeterminateProgress = false;
            this.uploadProgress = Math.round(events.loaded / events.total * 100);
          } else if (events.type === HttpEventType.Response) {
            this.showIndeterminateProgress = false;
            // Updating values in session storage
            if (events.body.class_profile_picture) {
              sessionStorage.setItem('class_profile_picture_id', events.body.id);
              sessionStorage.setItem('class_profile_picture', events.body.image);
              sessionStorage.setItem('class_profile_picture_uploaded_on', events.body.uploaded_on);
              this.pictureSuccessfullyUploaded.classProfilePictureChanged = true;
            }
            if (events.body.public_profile_picture) {
              sessionStorage.setItem('public_profile_picture_id', events.body.id);
              sessionStorage.setItem('public_profile_picture', events.body.image);
              sessionStorage.setItem('public_profile_picture_uploaded_on', events.body.uploaded_on);
            }
            this.pictureSuccessfullyUploaded.status = true;

            // Closing the dialog
            document.getElementById('closeDialogueButton').click();
          }
        },
        errors => {
          if (errors.error.non_field_errors) {
            this.choosePictureTarget = errors.error.non_field_errors[0];
          } else {
            console.log(errors);
            this.choosePictureTarget = 'Error!! Unable to upload profile picture.';
          }
        }
      );
    } else {
      this.choosePictureTarget = 'Select where you want to apply the picture';
    }
  }
}
