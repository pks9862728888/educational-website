import { STUDY_MATERIAL_CONTENT_TYPE_REVERSE } from 'src/constants';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { baseUrl } from '../../urls';
import { CookieService } from 'ngx-cookie-service';
import { Injectable } from '@angular/core';
import { authTokenName } from './../../constants';
import { PaymentSuccessCallbackResponse } from './../license/license.model';

interface FormDataInterface {
  name: string;
  country: string;
  institute_category: string;
  institute_profile: {
    motto: string;
    email: string;
    phone: string;
    website_url: string;
    state: string;
    pin: string;
    address: string;
    recognition: string;
    primary_language: string;
    secondary_language: string;
    tertiary_language: string;
  };
}

interface InviterUserInterface {
  role: string;
  invitee: string;
}


@Injectable({
  providedIn: 'root'
})
export class InstituteApiService {

  // Urls for communicating with backend
  baseUrl = baseUrl;
  instituteBaseUrl = `${baseUrl}institute/`;
  instituteMinDetailsAdminUrl = `${this.instituteBaseUrl}institute-min-details-teacher-admin`;
  instituteJoinedDetailUrl = `${this.instituteBaseUrl}joined-institutes-teacher`;
  institutePendingInvitesUrl = `${this.instituteBaseUrl}pending-institute-invites-teacher`;
  instituteCreateUrl = `${this.instituteBaseUrl}create`;
  studentInstituteMinDetailsUrl = `${this.instituteBaseUrl}institute-min-details-student`;

  // Insitute license related urls
  instituteLicenseListUrl = `${this.instituteBaseUrl}institute-license-list`;
  instituteSelectedLicenseDetail = `${this.instituteBaseUrl}institute-license-detail`;
  instituteDiscountCouponDetailUrl = `${this.instituteBaseUrl}get-discount-coupon`;
  licenseSelectPlanUrl = `${this.instituteBaseUrl}select-license`;
  createLicensePurchaseOrderUrl = `${this.instituteBaseUrl}create-order`;
  razorpayCallbackUrl = `${this.instituteBaseUrl}razorpay-payment-callback`;

  // Institute class related urls
  addClassPermissionUrl = `${this.instituteBaseUrl}add-class-permission`;

  // Institute subject related urls
  addSubjectInchargeUrl = `${this.instituteBaseUrl}add-subject-permission`;

  // Institute section related urls
  addSectionInchargeUrl = `${this.instituteBaseUrl}add-section-permission`;

  getInstituteDetailUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}detail/${instituteSlug}`;
  }

  getUserListUrl(instituteSlug: string, role: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/${role}/get-user-list`;
  }

  getUserInviteUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/provide-permission`;
  }

  getInstituteJoinDeclineUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/accept-delete-permission`;
  }

  getInstituteLicensePurchasedUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/get-license-purchased`;
  }

  getPaidInstituteLicenseUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/check-license-exists`;
  }

  getInstituteClassListUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/list-all-class`;
  }

  getClassListSlugAndNameListUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/get-class-slug-name-pairs`;
  }

  createInstituteClassUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/create-class`;
  }

  createDeleteClassUrl(classSlug: string) {
    return `${this.instituteBaseUrl}${classSlug}/delete-class`;
  }

  getInstituteClassPermissionListUrl(classSlug: string) {
    return `${this.instituteBaseUrl}${classSlug}/list-class-incharges`;
  }

  // Subject related urls
  createSubjectUrl(subjectSlug: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/create-subject`;
  }

  getInstituteSubjectListUrl(classSlug: string) {
    return `${this.instituteBaseUrl}${classSlug}/list-all-subject`;
  }

  getCourseMinDetailsUrl(subjectSlug: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/subject-course-content-min-statistics`;
  }

  getAddWeekInSubjectModuleUrl(subjectSlug: string){
    return `${this.instituteBaseUrl}${subjectSlug}/add-week`;
  }

  getDeleteWeekOfSubjectModuleUrl(
     instituteSlug: string,
     subjectSlug: string,
     viewKey: string,
     week: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${viewKey}/${week}/delete-week`;
  }

  getCreateSubjectModuleUrl(subjectSlug: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/add-view`;
  }

  getEditSubjectModuleUrl(subjectSlug: string, viewKey: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${viewKey}/edit-subject-view-name`;
  }

  getDeleteSubjectModuleUrl(
    instituteSlug: string,
    subjectSlug: string,
    viewKey: string,
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${viewKey}/delete-subject-view`;
  }

  addSubjectCourseContentUrl(subjectSlug: string){
    return `${this.instituteBaseUrl}${subjectSlug}/add-subject-course-content`;
  }

  editSubjectCourseContentUrl(subjectSlug: string, pk: number) {
    return `${this.instituteBaseUrl}${subjectSlug}/${pk}/edit-subject-course-content`;
  }

  getCourseContentOfSpecificViewUrl(subjectSlug: string, viewKey: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${viewKey}/list-subject-specific-view-course-contents`;
  }

  getDeleteCourseContentUrl(pk: string) {
    return `${this.instituteBaseUrl}${pk}/delete-subject-course-content`;
  }

  // Subject course preview related urls
  getMinSubjectCoursePreviewDetailsUrl(instituteSlug: string, subjectSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/subject-course-preview-min-details`;
  }

  getInstituteSpecificCourseContentPreviewUrl(
    instituteSlug: string,
    subjectSlug: string,
    viewKey: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${viewKey}/preview-subject-specific-view-contents`;
  }

  // Section related urls
  createSectionUrl(classSlug: string) {
    return `${this.instituteBaseUrl}${classSlug}/create-section`;
  }

  getSectionListUrl(classSlug: string) {
    return `${this.instituteBaseUrl}${classSlug}/list-all-section`;
  }

  getSubjectInchargeListUrl(subjectSlug: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/list-subject-instructors`;
  }

  getSectionInchargeListUrl(sectionSlug: string) {
    return `${this.instituteBaseUrl}${sectionSlug}/list-section-incharges`;
  }

  // Institute Students url
  getInstituteStudentAddUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/add-student-to-institute`;
  }

  getInstituteStudentsListUrl(instituteSlug: string, studentType: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/student-list/${studentType}`;
  }

  getEditInstituteStudentDetailsUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/edit-institute-student-details`;
  }

  getLoadStudentConfrimProfileDetailsUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/get-institute-student-user-profile-details`;
  }

  constructor( private cookieService: CookieService,
               private httpClient: HttpClient ) { }

  // Get minimum details of institute for admin teacher of institute
  getTeacherAdminInstituteMinDetails() {
    return this.httpClient.get(this.instituteMinDetailsAdminUrl, {headers: this.getAuthHeader()});
  }

  getJoinedInstituteMinDetails() {
    return this.httpClient.get(this.instituteJoinedDetailUrl, {headers: this.getAuthHeader()});
  }

  getInvitedInstituteMinDetails() {
    return this.httpClient.get(this.institutePendingInvitesUrl, {headers: this.getAuthHeader()});
  }

  // Create an institute
  createInstitute(fromData: FormDataInterface) {
    return this.httpClient.post(this.instituteCreateUrl, JSON.stringify(fromData), {headers: this.getAuthHeader()});
  }

  // Get institute details
  getInstituteDetails(instituteSlug: string) {
    return this.httpClient.get(this.getInstituteDetailUrl(instituteSlug), {headers: this.getAuthHeader()});
  }

  // Get list of admins
  getUserList(instituteSlug: string, role:string) {
    return this.httpClient.get(
      this.getUserListUrl(instituteSlug, role),
      { headers: this.getAuthHeader() });
  }

  // Invite new user
  inviteUser(instituteSlug: string, payload: InviterUserInterface) {
    return this.httpClient.post(
      this.getUserInviteUrl(instituteSlug), payload,
      { headers: this.getAuthHeader() }
    );
  }

  // Decline invitation
  acceptDeleteInstituteJoinInvitation(instituteSlug: string, operation: string) {
    return this.httpClient.post(
      this.getInstituteJoinDeclineUrl(instituteSlug),
      { 'operation': operation.toUpperCase()},
      { headers: this.getAuthHeader() }
    );
  }

  // Get institute license list
  getInstituteLicenseList() {
    return this.httpClient.get(
      this.instituteLicenseListUrl,
      { 'headers': this.getAuthHeader() });
  }

  // Get specific license details
  getSelectedLicenseDetails(id: string) {
    return this.httpClient.post(
      this.instituteSelectedLicenseDetail,
      {'id': id},
      { headers: this.getAuthHeader() }
    );
  }

  // Get coupon details
  getDiscountCouponDetails(couponCode: string) {
    return this.httpClient.post(
      this.instituteDiscountCouponDetailUrl,
      { 'coupon_code': couponCode },
      { headers: this.getAuthHeader() }
    );
  }

  // To initiate purchase request
  purchase(institute_slug: string, license_id: string, coupon_code: string) {
    return this.httpClient.post(
      this.licenseSelectPlanUrl,
      { 'institute_slug': institute_slug, 'license_id': license_id, 'coupon_code': coupon_code },
      { headers: this.getAuthHeader() }
    );
  }

  // To create order for license purchase
  createOrder(instituteSlug: string, selectedLicensePlanId: string, paymentGateway: string) {
    return this.httpClient.post(
      this.createLicensePurchaseOrderUrl,
      {
        'institute_slug': instituteSlug,
        'payment_gateway': paymentGateway,
        'license_id': selectedLicensePlanId
      },
      { headers: this.getAuthHeader() }
    );
  }

  // To send razorpay callback to server
  sendCallbackAndVerifyPayment(data: PaymentSuccessCallbackResponse, order_details_id: string) {
    return this.httpClient.post(
      this.razorpayCallbackUrl,
      {
        'razorpay_order_id': data.razorpay_order_id,
        'razorpay_payment_id': data.razorpay_payment_id,
        'razorpay_signature': data.razorpay_signature,
        'order_details_id': order_details_id
      },
      { headers: this.getAuthHeader() }
    );
  }

  // To get license purchase details of institue
  getInstituteLicensePurchased(instituteSlug: string) {
    return this.httpClient.get(
      this.getInstituteLicensePurchasedUrl(instituteSlug),
      { headers: this.getAuthHeader() }
    );
  }

  // To get paid unexpired license details
  getPaidUnexpiredLicenseDetails(instituteSlug: string) {
    return this.httpClient.get(
      this.getPaidInstituteLicenseUrl(instituteSlug),
      { headers: this.getAuthHeader() }
    )
  }

  // To get all institute class list
  getInstituteClassList(instituteSlug: string) {
    return this.httpClient.get(
      this.getInstituteClassListUrl(instituteSlug),
      { headers: this.getAuthHeader() }
    );
  }

  createInstituteClass(instituteSlug: string, name: string) {
    return this.httpClient.post(
      this.createInstituteClassUrl(instituteSlug),
      { 'name': name },
      { headers: this.getAuthHeader() }
    );
  }

  getInstituteClassKeyValuePairs(instituteSlug: string) {
    return this.httpClient.get(
      this.getClassListSlugAndNameListUrl(instituteSlug),
      { headers: this.getAuthHeader() }
    );
  }

  // To delete class
  deleteClass(classSlug: string) {
    return this.httpClient.delete(
      this.createDeleteClassUrl(classSlug),
      { headers: this.getAuthHeader() }
    );
  }

  // To get list of class incharges
  getClassInchargeList(classSlug: string) {
    return this.httpClient.get(
      this.getInstituteClassPermissionListUrl(classSlug),
      { headers: this.getAuthHeader()}
    )
  }

  // To add class incharge
  addClassIncharge(invitee: string, classSlug: string) {
    return this.httpClient.post(
      this.addClassPermissionUrl,
      { 'invitee': invitee, 'class_slug': classSlug },
      { headers: this.getAuthHeader() }
    );
  }

  // Subject related methods
  createSubject(classSlug: string, name: string, type: string) {
    return this.httpClient.post(
      this.createSubjectUrl(classSlug),
      {
        'name': name,
        'type': type
      },
      { headers: this.getAuthHeader() }
    );
  }

  getSubjectList(classSlug: string) {
    return this.httpClient.get(
      this.getInstituteSubjectListUrl(classSlug),
      { headers: this.getAuthHeader() }
    );
  }

  getInstituteSubjectInchargeList(subjectSlug: string) {
    return this.httpClient.get(
      this.getSubjectInchargeListUrl(subjectSlug),
      { headers: this.getAuthHeader() }
    );
  }

  addSubjectIncharge(invitee: string, subjectSlug: string) {
    return this.httpClient.post(
      this.addSubjectInchargeUrl,
      { 'invitee': invitee, 'subject_slug': subjectSlug },
      { headers: this.getAuthHeader() }
    );
  }

  // To create institute section
  createClassSection(classSlug: string, name: string) {
    return this.httpClient.post(
      this.createSectionUrl(classSlug),
      {'name': name},
      { headers: this.getAuthHeader() }
    );
  }

  getInstituteSectionList(classSlug: string) {
    return this.httpClient.get(
      this.getSectionListUrl(classSlug),
      { headers: this.getAuthHeader() }
    );
  }

  getInstituteSectionInchargeList(sectionSlug: string) {
    return this.httpClient.get(
      this.getSectionInchargeListUrl(sectionSlug),
      { headers: this.getAuthHeader() }
    );
  }

  addSectionIncharge(invitee: string, sectionSlug: string) {
    return this.httpClient.post(
      this.addSectionInchargeUrl,
      { 'invitee': invitee, 'section_slug': sectionSlug },
      { headers: this.getAuthHeader() }
    );
  }

  // To create course
  getMinCourseDetails(subjectSlug: string) {
    return this.httpClient.get(
      this.getCourseMinDetailsUrl(subjectSlug),
      { headers: this.getAuthHeader() }
    );
  }

  addSubjectModuleWeek(subjectSlug: string, viewKey: string) {
    return this.httpClient.post(
      this.getAddWeekInSubjectModuleUrl(subjectSlug),
      {'view_key': viewKey},
      { headers: this.getAuthHeader() }
    );
  }

  deleteWeekOfSubjectModule(
    instituteSlug: string,
    subjectSlug: string,
    viewKey: string,
    week: string) {
      return this.httpClient.delete(
        this.getDeleteWeekOfSubjectModuleUrl(
          instituteSlug,
          subjectSlug,
          viewKey,
          week
        ),
        { headers: this.getAuthHeader() }
      );
  }

  createSubjectModule(
    subjectSlug: string,
    name: string
  ) {
    return this.httpClient.post(
      this.getCreateSubjectModuleUrl(subjectSlug),
      {'name': name},
      { headers: this.getAuthHeader() }
    );
  }

  editSubjectModuleName(
    subjectSlug: string,
    viewKey: string,
    moduleName: string
  ) {
    return this.httpClient.patch(
      this.getEditSubjectModuleUrl(subjectSlug, viewKey),
      {'name': moduleName},
      { headers: this.getAuthHeader() }
    );
  }

  deleteSubjectModule(
    instituteSlug: string,
    subjectSlug: string,
    viewKey: string
  ) {
    return this.httpClient.delete(
      this.getDeleteSubjectModuleUrl(
        instituteSlug,
        subjectSlug,
        viewKey
      ),
      { headers: this.getAuthHeader() }
    );
  }

  addSubjectExternalLinkCourseContent(subjectSlug: string, data: any) {
    return this.httpClient.post(
      this.addSubjectCourseContentUrl(subjectSlug),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  uploadStudyMaterial(subjectSlug: string, data: any) {
    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('view_key', data.view_key);
    formData.append('size', data.size);
    formData.append('file', data.file);
    formData.append('content_type', data.content_type);

    if (data.week) {
      formData.append('week', data.week);
    }

    if (data.description) {
      formData.append('description', data.description);
    }

    if (data.content_type !== STUDY_MATERIAL_CONTENT_TYPE_REVERSE['EXTERNAL_LINK']) {
      formData.append('can_download', data.can_download);
    }

    if (data.target_date) {
      formData.append('target_date', data.target_date);
    }

    return this.httpClient.post(
      this.addSubjectCourseContentUrl(subjectSlug),
      formData,
      {
        headers: this.getAuthTokenHeader(),
        reportProgress: true,
        observe: 'events'
      }
    );
  }

  editSubjectCourseContent(data: any, subjectSlug:string, pk: number) {
    return this.httpClient.patch(
      this.editSubjectCourseContentUrl(subjectSlug, pk),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  getCourseContentOfSpecificView(subjectSlug: string, viewKey: string) {
    return this.httpClient.get(
      this.getCourseContentOfSpecificViewUrl(subjectSlug, viewKey),
      { headers: this.getAuthHeader() }
    );
  }

  deleteClassCourseContent(pk: string) {
    return this.httpClient.delete(
      this.getDeleteCourseContentUrl(pk),
      { headers: this.getAuthHeader() }
    );
  }

  // Course preview
  getMinSubjectCoursePreviewDetails(instituteSlug: string, subjectSlug: string) {
    return this.httpClient.get(
      this.getMinSubjectCoursePreviewDetailsUrl(instituteSlug, subjectSlug),
      {headers: this.getAuthHeader()}
    );
  }

  getInstituteSpecificCourseContentPreview(
    instituteSlug: string,
    subjectSlug: string,
    viewKey: string) {
      return this.httpClient.get(
        this.getInstituteSpecificCourseContentPreviewUrl(
          instituteSlug,
          subjectSlug,
          viewKey
        ),
        {headers: this.getAuthHeader()}
      );
  }

  // Institute Student
  inviteStudentToInstitute(
    instituteSlug: string,
    data: any
  ) {
    return this.httpClient.post(
      this.getInstituteStudentAddUrl(instituteSlug),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  getInstituteStudentsList(
    instituteSlug: string,
    studentType: string
  ) {
    return this.httpClient.get(
      this.getInstituteStudentsListUrl(instituteSlug, studentType),
      { headers: this.getAuthHeader() }
    );
  }

  editInstituteStudentDetails(
    instituteSlug: string,
    data: any
  ) {
    return this.httpClient.patch(
      this.getEditInstituteStudentDetailsUrl(instituteSlug),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  getInstituteMinDetailsStudent() {
    return this.httpClient.get(
      this.studentInstituteMinDetailsUrl,
      {headers: this.getAuthHeader()}
    );
  }

  loadStudentConfirmProfileDetails(instituteSlug: string) {
    return this.httpClient.get(
      this.getLoadStudentConfrimProfileDetailsUrl(instituteSlug),
      { headers: this.getAuthHeader() }
    );
  }

  // To load token from storage
  loadToken() {
    return this.cookieService.get(authTokenName);
  }

  getAuthHeader() {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Token ${this.loadToken()}`
    });
  }

  getAuthTokenHeader() {
    return new HttpHeaders({
      Authorization: `Token ${this.loadToken()}`
    });
  }
}
