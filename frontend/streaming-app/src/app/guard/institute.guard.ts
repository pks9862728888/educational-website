import { INSTITUTE_TYPE_REVERSE } from './../../constants';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { Injectable } from '@angular/core';


@Injectable()
export class InstituteRoutingGuard implements CanActivate {
  // Activates link if unexpired license exists
  constructor(private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    console.log('**************************');
    if(sessionStorage.getItem('purchasedLicenseExists') === 'true') {
      return true;
    } else {
      const currentInstituteSlug = sessionStorage.getItem('currentInstituteSlug');
      const currentInstituteType = sessionStorage.getItem('currentInstituteType');
      if (currentInstituteType === INSTITUTE_TYPE_REVERSE['School']) {
        this.router.navigate(['/school-workspace/' + currentInstituteSlug + '/profile']);
      } else if (currentInstituteType === INSTITUTE_TYPE_REVERSE['College']) {
        this.router.navigate(['/college-workspace/' + currentInstituteSlug + '/profile']);
      } else if (currentInstituteType === INSTITUTE_TYPE_REVERSE['Coaching']) {
        this.router.navigate(['/coaching-workspace/' + currentInstituteSlug + '/profile']);
      }
    }
  }
}
