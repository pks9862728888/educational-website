import { InAppDataTransferService } from '../../services/in-app-data-transfer.service';
import { ApiService } from '../../services/api.service';
import { Component, OnInit, } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';
import { ImageCroppedEvent, base64ToFile } from 'ngx-image-cropper';
import { HttpEventType } from '@angular/common/http';
import { ImageUploadResponse } from '../../models/profile.model';


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

  // For cropping image to visible ratio
  imageChangedEvent: any = '';

  constructor(
    private media: MediaMatcher,
    private apiService: ApiService,
    private inAppDataTransferService: InAppDataTransferService
  ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {}

  resetEvents() {
    this.chosenFile = null;
    this.fileNotChosen = true;
    this.imageChangedEvent = null;
  }

  onProfilePictureSelected(event: any) {
    this.imageError = null;
    const file: File = (<HTMLInputElement>document.getElementById('image-file')).files[0];

    if (!file.type.includes('image/jpeg') && !file.type.includes('image/jpg') && !file.type.includes('image/png')) {
      this.imageError = 'Choose a valid image.';
      this.resetEvents();
    } else {
      const filename = event.target.files[0].name.toLowerCase().split('.');
      const extension = filename[filename.length - 1];
      const regex = new RegExp('^(jpeg|png|jpg)$');
      if (regex.test(extension)) {
        if (event.target.files[0].size !== 0 ) {
          this.chosenFile = event.target.files[0].name;
          this.imageChangedEvent = event;
          this.fileNotChosen = false;
          this.imageError = null;
        } else {
          this.resetEvents();
          this.imageError = 'Choose a valid image.';
        }
      } else {
        this.resetEvents();
        this.imageError = 'Invalid image.';
      }
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
            this.showIndeterminateProgress = false;
            this.uploadProgress = Math.round(events.loaded / events.total * 100);
          } else if (events.type === HttpEventType.Response) {
            this.inAppDataTransferService.sendProfilePictureUpdatedData(events.body);
            this.showIndeterminateProgress = false;
            document.getElementById('closeDialogueButton').click();
          }
        },
        errors => {
          if (errors.error) {
            if (errors.error.non_field_errors) {
              this.choosePictureTarget = errors.error.non_field_errors[0];
            } else {
              this.choosePictureTarget = 'Error!! Unable to upload profile picture.';
            }
          }
        }
      );
    } else {
      this.choosePictureTarget = 'Select where you want to apply the picture.';
    }
  }
}
