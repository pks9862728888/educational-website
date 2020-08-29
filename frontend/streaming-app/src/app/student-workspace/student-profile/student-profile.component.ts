import { Component, OnInit } from '@angular/core';
import { formatDate } from 'src/app/format-datepicker';
import { Validators, FormBuilder, FormGroup } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { MediaMatcher } from '@angular/cdk/layout';
import { Subscription } from 'rxjs';
import { InAppDataTransferService } from '../../services/in-app-data-transfer.service';
import { ApiService } from '../../services/api.service';
import { UiService } from '../../services/ui.service';
import { getGender, getCountry, getLanguage } from '../../shared/utilityFunctions';
import { UserProfileDetails, DeletedCurrentPictureResponse } from '../../models/profile.model';
import { UploadProfilePictureComponent } from 'src/app/teacher-workspace/teacher-profile/upload-profile-picture/upload-profile-picture.component';
import { ChooseFromExistingComponent } from 'src/app/teacher-workspace/teacher-profile/choose-from-existing/choose-from-existing.component';

@Component({
  selector: 'app-student-profile',
  templateUrl: './student-profile.component.html',
  styleUrls: ['./student-profile.component.css']
})
export class StudentProfileComponent implements OnInit {

  // For detecting whether device is mobile
  mq: MediaQueryList;
  showLoadingIndicator: boolean;
  showReloadIndicator: boolean;

  // For controlling edit views
  editProfile = false;
  editAccount = false;
  editProfilePicture = false;
  profilePictureCount: number;

  // Edit Forms
  editProfileForm: FormGroup;

  // Response data of user profile
  userProfileData: UserProfileDetails;

  // For showing errors
  usernameError: string;
  phoneNumberError: string;

  // Controls the maximum date of birth allowed
  maxDate: Date;
  profilePictureUpdatedDataSubscription: Subscription;
  getLanguage = getLanguage;
  getCountry = getCountry;
  getGender = getGender;

  constructor(
    private media: MediaMatcher,
    private apiService: ApiService,
    private uiService: UiService,
    private formBuilder: FormBuilder,
    private inAppDataTransferService: InAppDataTransferService,
    private dialog: MatDialog ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.maxDate = new Date();         // For selecting max date as today
  }

  ngOnInit(): void {
    this.fetchUserData();

    // For getting the total number of profile picture count from server
    this.apiService.getProfilePictureCount().subscribe(
      (result: {count: number; }) => {
        this.profilePictureCount = result.count;
      },
      error => {}
    );
  }

  fetchUserData() {
    this.showLoadingIndicator = true;
    this.apiService.getTeacherProfile().subscribe(
      (result: UserProfileDetails) => {
        this.showLoadingIndicator = false;
        sessionStorage.setItem('user_id', result.id.toString());
        this.userProfileData = result;
      },
      errors => {
        this.showLoadingIndicator = false;
        this.showReloadIndicator = true;
      }
    );
  }

  checkUserDataExists() {
    if (!this.userProfileData) {
      this.fetchUserData();
    }
  }

  createEditProfileForm() {
    this.editProfileForm = this.formBuilder.group({
      username: [this.userProfileData.username, [
        Validators.required,
        Validators.minLength(4),
        Validators.maxLength(30)
      ]],
      user_profile: this.formBuilder.group({
        first_name: [this.userProfileData.user_profile.first_name, [Validators.required] ],
        last_name: [this.userProfileData.user_profile.last_name, [Validators.required]],
        phone: [this.userProfileData.user_profile.phone, ],
        gender: [this.userProfileData.user_profile.gender, [Validators.required]],
        country: [this.userProfileData.user_profile.country, [Validators.required]],
        date_of_birth: [this.userProfileData.user_profile.date_of_birth, [Validators.required]],
        primary_language: [this.userProfileData.user_profile.primary_language, [Validators.required]],
        secondary_language: [this.userProfileData.user_profile.secondary_language, ],
        tertiary_language: [this.userProfileData.user_profile.tertiary_language, ]
      })
    });
  }

  editProfileClicked() {
    if (this.editProfile === false) {
      this.createEditProfileForm();
    }
    this.editProfile = !this.editProfile;
  }

  profileDetailsReset() {
    this.editProfileForm.patchValue({
      username: this.userProfileData.username,
      user_profile: {
        first_name: this.userProfileData.user_profile.first_name,
        last_name: this.userProfileData.user_profile.last_name,
        phone: this.userProfileData.user_profile.phone,
        gender: this.userProfileData.user_profile.gender,
        country: this.userProfileData.user_profile.country,
        date_of_birth: this.userProfileData.user_profile.date_of_birth,
        primary_language: this.userProfileData.user_profile.primary_language,
        secondary_language: this.userProfileData.user_profile.secondary_language,
        tertiary_language: this.userProfileData.user_profile.tertiary_language
      }
    });
  }

  profileDetailsSubmit() {
    this.editProfileForm.patchValue({
      username: this.editProfileForm.value.username.trim(),
      user_profile: {
        first_name: this.editProfileForm.value.user_profile.first_name.trim(),
        last_name: this.editProfileForm.value.user_profile.last_name.trim(),
      }
    });
    if (!this.editProfileForm.invalid) {
      const editProfileDetailsData = this.editProfileForm.value;
      if (editProfileDetailsData.user_profile.date_of_birth) {
        // Formatting date of birth in YYYY-MM-DD
        editProfileDetailsData.user_profile.date_of_birth = formatDate(this.editProfileForm.value.user_profile.date_of_birth);
      }

      this.apiService.patchTeacherProfileDetails(editProfileDetailsData).subscribe(
        (result: UserProfileDetails ) => {
          this.userProfileData.username = result.username;
          this.userProfileData.user_profile.country = result.user_profile.country;
          this.userProfileData.user_profile.date_of_birth = result.user_profile.date_of_birth;
          this.userProfileData.user_profile.first_name = result.user_profile.first_name;
          this.userProfileData.user_profile.last_name = result.user_profile.last_name;
          this.userProfileData.user_profile.gender = result.user_profile.gender;
          this.userProfileData.user_profile.phone = result.user_profile.phone;
          this.userProfileData.user_profile.primary_language = result.user_profile.primary_language;
          this.userProfileData.user_profile.secondary_language = result.user_profile.secondary_language;
          this.userProfileData.user_profile.tertiary_language = result.user_profile.tertiary_language;
          this.uiService.showSnackBar('Profile details updated successfully!', 2000);
          this.editProfile = !this.editProfile;
        },
        errors => {
          if (errors.error) {
            if (errors.error.user_profile.phone) {
              this.phoneNumberError = errors.error.user_profile.phone[0];
            }
            if (errors.error.username) {
              this.usernameError = errors.error.username[0];
            }
          }
        }
      );
    } else {
      this.uiService.showSnackBar('Form contains invalid data!', 2500);
    }
  }

  editAccountClicked() {
    this.editAccount = !this.editAccount;
  }

  openEditProfilePictureDialog() {
    this.editProfilePicture = !this.editProfilePicture;
  }

  updateProfilePictureData(data: any) {
    if (data['class_profile_picture']) {
      this.userProfileData.profile_pictures.id = data.id;
      this.userProfileData.profile_pictures.image = data.image;
      this.userProfileData.profile_pictures.uploaded_on = data.uploaded_on;
    }
    this.uiService.showSnackBar(
      'Profile picture uploaded successfully!',
      2000
    );
    if (!data.dont_update_count) {
      if (this.profilePictureCount) {
        this.profilePictureCount += 1;
      } else {
        this.profilePictureCount = 1;
      }
    }
    this.editProfilePicture = false;
  }

  openUploadPictureDialog() {
    const dialogRef = this.dialog.open(UploadProfilePictureComponent);

    this.profilePictureUpdatedDataSubscription = this.inAppDataTransferService.profilePictureUpdatedData$.subscribe(
      data => {
        this.updateProfilePictureData(data);
      }
    );

    dialogRef.afterClosed().subscribe(result => {
      if (this.profilePictureUpdatedDataSubscription) {
        this.profilePictureUpdatedDataSubscription.unsubscribe();
      }
    });
  }

  // To delete the current active class profile picture
  deleteCurrentPicture() {
    const id = this.userProfileData.profile_pictures.id;

    this.apiService.deleteCurrentProfilePicture(id.toString()).subscribe(
      (response: DeletedCurrentPictureResponse) => {
        if (response.deleted === true) {
          if (response.class_profile_picture_deleted === true) {
            this.userProfileData.profile_pictures.image = null;
          }
          if (this.profilePictureCount) {
            this.profilePictureCount -= 1;
          }
          this.editProfilePicture = false;
        }
        this.uiService.showSnackBar('Successfully deleted current profile picture.', 2000);
      },
      errors => {
        if (errors.error) {
          if (errors.error.id) {
            this.uiService.showSnackBar(errors.error.id, 2000);
          } else {
            this.uiService.showSnackBar('Unable to delete at the moment :(', 2000);
          }
        } else {
          this.uiService.showSnackBar('Unable to delete at the moment :(', 2000);
        }
      }
    );
  }

  // To remove the current active class profile picture
  removeCurrentPicture() {
    this.apiService.removeCurrentClassProfilePicture().subscribe(
      (response: {removed: boolean; } ) => {
        if (response.removed === true) {
          this.userProfileData.profile_pictures.image = null;
          this.userProfileData.profile_pictures.uploaded_on = null;
        }
        this.editProfilePicture = false;
      },
      error => {
        console.log(error);
      }
    );
  }

  // To choose from existing profile picture
  chooseFromExistingClicked() {
    const dialogRef = this.dialog.open(ChooseFromExistingComponent);

    this.profilePictureUpdatedDataSubscription = this.inAppDataTransferService.profilePictureUpdatedData$.subscribe(
      data => {
        data['dont_update_count'] = true;
        this.updateProfilePictureData(data);
      }
    );

    dialogRef.afterClosed().subscribe(result => {
      if (this.profilePictureUpdatedDataSubscription) {
        this.profilePictureUpdatedDataSubscription.unsubscribe();
      }
    });
  }
}
