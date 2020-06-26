import { Subscription } from 'rxjs';
import { InterModuleDataTransferService } from './../../inter-module-data-transfer.service';
import { COUNTRY, STATE, INSTITUTE_CATEGORY } from './../../../constants';
import { InstituteApiService } from './../../institute-api.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, OnDestroy } from '@angular/core';

interface TeacherAdminInstitutesMin {
  id: number;
  user: number;
  name: string;
  country: string;
  institute_category: string;
  created_date: string;
  institute_profile: {
    motto: string;
    email: string;
    phone: string;
    website_url: string;
    state: string;
  };
  institute_logo: {
    image: string;
  };
  institute_statistics: {
    no_of_students: number;
    no_of_faculties: number;
    no_of_staff: number;
  };
}

@Component({
  selector: 'app-teacher-college',
  templateUrl: './teacher-college.component.html',
  styleUrls: ['./teacher-college.component.css']
})
export class TeacherCollegeComponent implements OnInit, OnDestroy {

  mobileQuery: MediaQueryList;

  // For handling filters
  appliedFilter = 'NONE';

  // For handling search results
  searched = false;

  // For handling views
  createInstituteClicked = false;

  // For handling expansion panel
  searchedInstituteStep: number;
  adminInstituteStep: number;
  joinedInstituteStep: number;

  // For handling star rating
  rating = 4;

  // For storing admin institutes
  teacherAdminInstitutesMinList: TeacherAdminInstitutesMin[] = [];

  // For handling views based on input from breadcrumb
  showInstituteListViewSubscription: Subscription;

  constructor(private media: MediaMatcher,
              private instituteApiService: InstituteApiService,
              private interModuleDataTransferService: InterModuleDataTransferService ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.instituteApiService.getTeacherAdminInstituteMinDetails().subscribe(
      (result: TeacherAdminInstitutesMin[]) => {
        for (const institute of result) {
          this.teacherAdminInstitutesMinList.push(institute);
        }
      },
      error => {
        console.error(error);
      }
    );

    // Subscribing to show the list view on input from breadcrumb
    this.showInstituteListViewSubscription = this.interModuleDataTransferService.setInstituteViewActive$.subscribe(
      (status: boolean) => {
        this.createInstituteClicked = false;
      }
    );
  }

  // For controlling expansion panel functioning
  setAdminInstituteStep(index: number) {
    this.adminInstituteStep = index;
  }

  setJoinedInstituteStep(index: number) {
    this.joinedInstituteStep = index;
  }

  setSearchedInstituteStep(index: number) {
    this.searchedInstituteStep = index;
  }

  // For checking filter
  checkFilter(filterName: string) {
    if (this.appliedFilter === filterName) {
      return true;
    } else {
      return false;
    }
  }

  applyFilter(filterName: string) {
    this.appliedFilter = filterName;
  }

  // Returns true if my institute list is empty, else false
  isMyInstituteEmpty() {
    return this.teacherAdminInstitutesMinList.length === 0;
  }

  // Decoding the respective keys
  decodeCountry(key: string) {
    return COUNTRY[key];
  }

  decodeState(key: string) {
    return STATE[key];
  }

  decodeCategory(key: string) {
    return INSTITUTE_CATEGORY[key];
  }

  createInstitute() {
    this.createInstituteClicked = true;
    this.interModuleDataTransferService.sendActiveBreadcrumbLinkData('CREATE');
  }

  // Taking action based on whether institute is created or not
  instituteCreated(event: boolean){
    if (event === true) {
      // If institute is created
    } else {
      this.createInstituteClicked = false;
      this.interModuleDataTransferService.sendActiveBreadcrumbLinkData('');
    }
  }

  ngOnDestroy() {
    this.showInstituteListViewSubscription.unsubscribe();
  }
}
