import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/api.service';
import { MediaMatcher } from '@angular/cdk/layout';

interface ImageDetails {
  id: number;
  image: string;
  uploaded_on: string;
  public_profile_picture: boolean;
  class_profile_picture: boolean;
}

interface SetProfilePictureResponse {
  id: string;
  image: string;
  class_profile_picture: boolean;
  uploaded_on: string;
  public_profile_picture: boolean;
}


@Component({
  selector: 'app-choose-from-existing',
  templateUrl: './choose-from-existing.component.html',
  styleUrls: ['./choose-from-existing.component.css']
})
export class ChooseFromExistingComponent implements OnInit {

  // For detecting whether device is mobile
  mobileQuery: MediaQueryList;

  // For storing image list
  imageList: ImageDetails[] = [];
  selectedImageId: string;
  selectedImageUrl: string;
  selectedImageUploadedOn: string;
  alsoSetAsPrivateProfilePicture: false;

  // For controlling the html layout
  showLoading = true;

  // Response to send to parent element while closing
  response = {
    status: false,
    classProfilePictureChanged: false,
  };

  constructor(private media: MediaMatcher,
              private apiService: ApiService) {
      this.mobileQuery = media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    // Fetching the list of images uploaded by the user
    this.apiService.listProfilePicture().subscribe(
      (response: ImageDetails[]) => {
        for (const image of response) {
          this.imageList.push(image);
        }
        this.showLoading = false;
        console.log(this.imageList);
      },
      error => {
        console.error(error);
      }
    );
  }

  imageClicked(id: string) {
    this.selectedImageId = id;

    for (const image of this.imageList) {
      if (image.id === Number(this.selectedImageId)) {
        this.selectedImageUrl = image.image;
        this.selectedImageUploadedOn = image.uploaded_on;
        break;
      }
    }
  }

  setProfilePicture() {
    const data = {
      id: this.selectedImageId,
      class_profile_picture: true,
      public_profile_picture: this.alsoSetAsPrivateProfilePicture
    };

    this.apiService.setUserProfilePicture(data).subscribe(
      (response: SetProfilePictureResponse) => {
        if (response.class_profile_picture) {
          sessionStorage.setItem('class_profile_picture_id', response.id);
          sessionStorage.setItem('class_profile_picture', response.image);
          sessionStorage.setItem('class_profile_picture_uploaded_on', response.uploaded_on);
          this.response.classProfilePictureChanged = true;
        }
        if (response.public_profile_picture) {
          sessionStorage.setItem('public_profile_picture_id', response.id);
          sessionStorage.setItem('public_profile_picture', response.image);
          sessionStorage.setItem('public_profile_picture_uploaded_on', response.uploaded_on);
        }
        this.response.status = true;

        // Closing the dialog
        document.getElementById('closeDialogueButton').click();
      },
      error => {
        console.log(error);
      }
    );
  }

  backClicked() {
    this.selectedImageId = null;
    this.selectedImageUrl = null;
    this.selectedImageUploadedOn = null;
  }
}
