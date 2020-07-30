import { INSTITUTE_TYPE_REVERSE } from '../../constants';
import { Router, CanActivate, RouterStateSnapshot, ActivatedRouteSnapshot } from '@angular/router';
import { Injectable } from '@angular/core';


@Injectable()
export class LicenseReviewGuard implements CanActivate {

  constructor( private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    if (sessionStorage.getItem('selectedLicenseId')) {
      return true;
    } else {
      const currentInstituteSlug = sessionStorage.getItem('currentInstituteSlug')
      if (currentInstituteSlug) {
        const instituteType = sessionStorage.getItem('currentInstituteType');
        if (instituteType) {
          sessionStorage.setItem('activeRoute', 'LICENSE');
          if (instituteType === INSTITUTE_TYPE_REVERSE['School']) {
            this.router.navigate(['school-workspace/' + currentInstituteSlug + 'license']);
          } else if (instituteType === INSTITUTE_TYPE_REVERSE['College']) {
            this.router.navigate(['college-workspace/' + currentInstituteSlug + 'license']);
          } else {
            this.router.navigate(['coaching-workspace/' + currentInstituteSlug + 'license']);
          }
        } else {
          sessionStorage.setItem('activeRoute', 'INSTITUTES');
          this.router.navigate(['teacher-workspace/institutes']);
        }
      } else {
        sessionStorage.setItem('activeRoute', 'INSTITUTES');
        this.router.navigate(['teacher-workspace/institutes']);
      }
    }
  }
}
