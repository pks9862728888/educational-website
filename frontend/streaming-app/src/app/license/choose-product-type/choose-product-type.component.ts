import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { InstituteApiService } from 'src/app/services/institute-api.service';

@Component({
  selector: 'app-choose-product-type',
  templateUrl: './choose-product-type.component.html',
  styleUrls: ['./choose-product-type.component.css']
})
export class ChooseProductTypeComponent implements OnInit {

  mq: MediaQueryList;
  currentUrlPath: string;

  constructor(
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService,
    private router: Router
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentUrlPath = window.location.pathname;
  }

  ngOnInit(): void {
  }

  navigateToInstituteLicenseDetails() {
    const loc = this.currentUrlPath.slice(0, this.currentUrlPath.length - '/choose-product-type'.length);
    this.router.navigate([loc]);
  }

  navigateToPurchaseCommonLicense() {
    const loc = this.currentUrlPath.slice(0, this.currentUrlPath.length - '/choose-product-type'.length);
    this.router.navigate([ loc + '/purchase-common-license' ]);
  }

  navigateToPurchaseDigitalExamLicense() {
    const loc = this.currentUrlPath.slice(0, this.currentUrlPath.length - '/choose-product-type'.length);
    this.router.navigate([ loc + '/purchase-digital-adaptive-exam-license' ]);
  }

  navigateToPurchaseLiveClassLicense() {
    const loc = this.currentUrlPath.slice(0, this.currentUrlPath.length - '/choose-product-type'.length);
    this.router.navigate([ loc + '/purchase-live-class-license' ]);
  }

  navigateToPurchaseStorageLicense() {
    const loc = this.currentUrlPath.slice(0, this.currentUrlPath.length - '/choose-product-type'.length);
    this.router.navigate([ loc + '/purchase-storage-license' ]);
  }

}
