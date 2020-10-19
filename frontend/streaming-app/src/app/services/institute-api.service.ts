import { LECTURE_STUDY_MATERIAL_TYPES, SUBJECT_INTRODUCTION_CONTENT_TYPE_REVERSE } from 'src/constants';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { baseUrl } from '../../urls';
import { CookieService } from 'ngx-cookie-service';
import { Injectable } from '@angular/core';
import { authTokenName } from './../../constants';
import { PaymentSuccessCallbackResponse } from '../models/license.model';

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
  bookmarkCourseUrl = `${this.instituteBaseUrl}bookmark-course`;

  // Insitute license related urls
  instituteCommonLicenseListUrl = `${this.instituteBaseUrl}institute-common-license-list`;
  instituteDiscountCouponDetailUrl = `${this.instituteBaseUrl}get-discount-coupon`;
  commonLicenseSelectPlanUrl = `${this.instituteBaseUrl}select-common-license`;
  createCommmonLicenseOrderUrl = `${this.instituteBaseUrl}create-common-license-order`;
  razorpayCommonLicenseCallbackUrl = `${this.instituteBaseUrl}razorpay-common-license-payment-callback`;
  razorpayStorageLicenseCallbackUrl = `${this.instituteBaseUrl}razorpay-storage-payment-callback`;

  // Institute class related urls
  addClassPermissionUrl = `${this.instituteBaseUrl}add-class-permission`;

  // Institute subject related urls
  addSubjectInchargeUrl = `${this.instituteBaseUrl}add-subject-permission`;
  allStudentCoursesUrl = `${this.instituteBaseUrl}list-all-student-institute-courses`;

  // Institute section related urls
  addSectionInchargeUrl = `${this.instituteBaseUrl}add-section-permission`;

  getDeleteUnpaidCommonLicenseUrl(instituteSlug: string, licenseOrderId: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/${licenseOrderId}/delete-unpaid-common-license`;
  }

  getStorageLicenseCredentialsForRetryPaymentUrl(instituteSlug: string, licenseOrderId: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/${licenseOrderId}/storage-license-credentials-for-retry-payment`;
  }

  getCommonLicenseCredentialsForRetryPaymentUrl(instituteSlug: string, licenseOrderId: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/${licenseOrderId}/common-license-credentials-for-retry-payment`;
  }

  getDeleteUnpaidStorageLicenseUrl(instituteSlug: string, licenseOrderId: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/${licenseOrderId}/delete-unpaid-storage-license`;
  }

  getStorageLicenseCredentialsUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/institute-storage-license-cost`;
  }

  getCreateStorageLicenseOrderUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/create-storage-license-order`;
  }

  getInstituteSelectedCommonLicenseDetailUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/institute-common-license-detail`;
  }

  getOrderedCommonLicenseDetailsUrl(instituteSlug: string, licenseId: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/${licenseId}/get-selected-common-license-details`;
  }

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

  getInstituteLicenseOrderDetailsUrl(instituteSlug: string, productType: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/${productType}/get-ordered-license-orders`;
  }

  getLicenseExistsStatisticsUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/license-exists-statistics`;
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

  addSubjectIntroductoryCourseContentUrl(subjectSlug: string){
    return `${this.instituteBaseUrl}${subjectSlug}/add-subject-introductory-content`;
  }

  editSubjectCourseContentUrl(subjectSlug: string, pk: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${pk}/edit-subject-introductory-content`;
  }

  getCourseContentOfSpecificViewUrl(subjectSlug: string, viewKey: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${viewKey}/list-subject-specific-view-course-contents`;
  }

  getDeleteSubjectIntroductoryContentUrl(subjectSlug: string, pk: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${pk}/delete-subject-introductory-content`;
  }

  getAddSubjectLectureUrl(subjectSlug: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/add-subject-lecture`;
  }

  getDeleteSubjectLectureUrl(subjectSlug: string, lectureId: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${lectureId}/delete-subject-lecture`;
  }

  getEditSubjectLectureUrl(subjectSlug: string, lectureId: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${lectureId}/edit-subject-lecture`;
  }

  getLoadSubjectLectureContentsUrl(subjectSlug: string, lectureId: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${lectureId}/list-subject-lecture-contents`;
  }

  getAddLectureObjectiveOrUseCaseUrl(subjectSlug: string, lectureId: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${lectureId}/add-lecture-objective-or-use-case-text`;
  }

  getDeleteObjectiveOrUseCaseUrl(subjectSlug: string, id: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${id}/delete-lecture-objective-or-use-case-text`;
  }

  getEditLectureObjectiveOrUseCaseUrl(subjectSlug: string, objectiveId: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${objectiveId}/edit-lecture-objective-or-use-case-text`;
  }

  getAddLectureAdditionalReadingOrUseCaseLinkUrl(subjectSlug: string, lectureId: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${lectureId}/add-lecture-use-case-or-additional-reading-link`;
  }

  getDeleteAdditionalReadingOrUseCaseLinkUrl(subjectSlug: string, linkId: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${linkId}/delete-lecture-use-case-or-additional-reading-link`;
  }

  getEditLectureAdditionalReadingOrUseCaseLinkUrl(subjectSlug: string, linkId: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${linkId}/edit-lecture-use-case-or-additional-reading-link`;
  }

  addLectureMaterialUrl(subjectSlug: string, lectureId: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${lectureId}/add-lecture-materials`;
  }

  getDeleteLectureContentUrl(subjectSlug: string, contentId: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${contentId}/delete-lecture-material`;
  }

  getEditLectureContentUrl(subjectSlug: string, contentId: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${contentId}/edit-lecture-material`;
  }

  getAddSubjectTestUrl(instituteSlug: string, subjectSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/add-test`;
  }

  getMinTestDetailsUrl(instituteSlug: string, subjectSlug: string, testSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${testSlug}/get-test-min-details`;
  }

  getTestMinDetailsForQuestionCreationUrl(subjectSlug: string, testSlug: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${testSlug}/get-test-details-for-question-paper-creation`;
  }

  getAddTestQuestionSetUrl(instituteSlug: string, subjectSlug: string, testSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${testSlug}/add-question-set`;
  }

  getDeleteTestFileUploadQuestionPaperUrl(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string
    ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${testSlug}/${setId}/delete-file-question-paper`;
  }

  getTestSetQuestionsUrl(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string
    ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${testSlug}/${setId}/get-question-set-questions`;
  }

  getDeleteQuestionSetUrl(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string
    ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${testSlug}/${setId}/delete-test-set`;
  }

  addTestConceptLabelUrl(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string
    ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${testSlug}/add-test-concept-label`;
  }

  deleteTestConceptLabelUrl(
    instituteSlug: string,
    subjectSlug: string,
    labelId: string
    ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${labelId}/delete-test-concept-label`;
  }

  addTestQuestionSectionUrl(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${testSlug}/${setId}/add-test-question-section`;
  }

  addImageTestQuestionUrl(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string,
    testSectionId: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${testSlug}/${setId}/${testSectionId}/upload-image-test-question`;
  }

  editImageTestQuestionUrl(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string,
    questionId: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${testSlug}/${setId}/${questionId}/edit-image-test-question`;
  }

  editQuestionSetUrl(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${testSlug}/${setId}/edit-question-set`;
  }

  deleteImageTestQuestionUrl(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string,
    questionId: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${testSlug}/${setId}/${questionId}/delete-image-test-question`;
  }

  getUploadFileQuestionPaperUrl(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string
    ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${testSlug}/${setId}/upload-file-question-paper`;
  }

  getClassStudentsListUrl(
    instituteSlug: string,
    classSlug: string,
    studentType: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${classSlug}/class-student-list/${studentType}`;
  }

  getSubjectStudentsListUrl(
    instituteSlug: string,
    classSlug: string,
    subjectSlug: string,
    studentType: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${classSlug}/${subjectSlug}/subject-student-list/${studentType}`;
  }

  getAskQuestionInCourseContentUrl(
    instituteSlug: string,
    subjectSlug: string,
    courseContentId: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${courseContentId}/ask-new-question`;
  }

  getLoadAllInstituteSubjectCourseContentQuestionsUrl(
    instituteSlug: string,
    subjectSlug: string,
    courseContentId: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${courseContentId}/list-questions`;
  }

  getLoadAnswerOfInstituteCourseQuestionUrl(
    instituteSlug: string,
    subjectSlug: string,
    questionId: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${questionId}/list-answers`;
  }

  getAnswerQuestionOfInstituteCourseContentUrl(
    instituteSlug: string,
    subjectSlug: string,
    questionId: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${questionId}/answer-question`;
  }

  getUpvoteDownvoteInstituteCourseContentQuestionUrl(
    instituteSlug: string,
    subjectSlug: string,
    questionId: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${questionId}/upvote-downvote-question`;
  }

  getUpvoteDownvoteInstituteCourseContentAnswerUrl(
    instituteSlug: string,
    subjectSlug: string,
    answerId: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/${answerId}/upvote-downvote-answer`;
  }

  getDeleteInstituteCourseContentAnswerUrl(subjectSlug: string, answerId: string) {
    return `${this.instituteBaseUrl}${subjectSlug}/${answerId}/delete-answer`;
  }

  getPinUnpinInstituteCourseContentAnswerUrl(answerId: string) {
    return `${this.instituteBaseUrl}${answerId}/pin-unpin-answer`;
  }

  getEditInstituteCourseContentAnswerUrl(
    insituteSlug: string,
    subjectSlug: string,
    answerId: string
  ) {
    return `${this.instituteBaseUrl}${insituteSlug}/${subjectSlug}/${answerId}/edit-answer`;
  }

  getEditInstituteCourseContentQuestionUrl(
    insituteSlug: string,
    subjectSlug: string,
    questionId: string
  ) {
    return `${this.instituteBaseUrl}${insituteSlug}/${subjectSlug}/${questionId}/edit-question`;
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
    return `${this.instituteBaseUrl}${instituteSlug}/institute-student-list/${studentType}`;
  }

  getEditInstituteStudentDetailsUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/edit-institute-student-details`;
  }

  getLoadStudentConfrimProfileDetailsUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/get-institute-student-user-profile-details`;
  }

  getStudentJoinInstituteUrl(instituteSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/join-institute-student`;
  }

  getInviteStudentToClassUrl(
    instituteSlug: string,
    classSlug: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${classSlug}/add-student-to-class`;
  }

  getInviteStudentToSubjectUrl(
    instituteSlug: string,
    classSlug: string,
    subjectSlug: string
  ) {
    return `${this.instituteBaseUrl}${instituteSlug}/${classSlug}/${subjectSlug}/add-student-to-subject`;
  }

  getCoursePeersUrl(instituteSlug: string, subjectSlug: string) {
    return `${this.instituteBaseUrl}${instituteSlug}/${subjectSlug}/list-subject-peers`;
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
  getUserList(instituteSlug: string, role: string) {
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
      { operation: operation.toUpperCase()},
      { headers: this.getAuthHeader() }
    );
  }

  // Get institute license list
  getInstituteCommonLicenseList(instituteSlug: string) {
    return this.httpClient.get(
      this.instituteCommonLicenseListUrl,
      { headers: this.getAuthHeader() });
  }

  getStorageLicenseCredentials(instituteSlug: string) {
    return this.httpClient.get(
      this.getStorageLicenseCredentialsUrl(instituteSlug),
      { headers: this.getAuthHeader() });
  }

  createStorageLicenseOrder(instituteSlug: string, data: any) {
    return this.httpClient.post(
      this.getCreateStorageLicenseOrderUrl(instituteSlug),
      data,
      { headers: this.getAuthHeader() }
    );
  }


  getSelectedCommonLicenseDetails(instituteSlug: string, id: string) {
    return this.httpClient.post(
      this.getInstituteSelectedCommonLicenseDetailUrl(instituteSlug),
      { id },
      { headers: this.getAuthHeader() }
    );
  }

  getOrderedCommonLicenseDetails(instituteSlug: string, licenseId: string) {
    return this.httpClient.get(
      this.getOrderedCommonLicenseDetailsUrl(instituteSlug, licenseId),
      { headers: this.getAuthHeader() }
    );
  }

  // Get coupon details
  getDiscountCouponDetails(couponCode: string) {
    return this.httpClient.post(
      this.instituteDiscountCouponDetailUrl,
      { coupon_code: couponCode },
      { headers: this.getAuthHeader() }
    );
  }

  // To initiate purchase request
  purchaseCommonLicense(instituteSlug: string, licenseId: string, couponCode: string) {
    return this.httpClient.post(
      this.commonLicenseSelectPlanUrl,
      { institute_slug: instituteSlug, license_id: licenseId, coupon_code: couponCode, current_time: +new Date() },
      { headers: this.getAuthHeader() }
    );
  }

  createCommonLicenseOrder(
    instituteSlug: string,
    selectedLicensePlanId: string,
    paymentGateway: string
    ) {
    return this.httpClient.post(
      this.createCommmonLicenseOrderUrl,
      {
        institute_slug: instituteSlug,
        payment_gateway: paymentGateway,
        license_id: selectedLicensePlanId
      },
      { headers: this.getAuthHeader() }
    );
  }

  sendCommonLicensePurchaseCallbackAndVerifyPayment(
    data: PaymentSuccessCallbackResponse,
    orderDetailsId: string
    ) {
    return this.httpClient.post(
      this.razorpayCommonLicenseCallbackUrl,
      {
        razorpay_order_id: data.razorpay_order_id,
        razorpay_payment_id: data.razorpay_payment_id,
        razorpay_signature: data.razorpay_signature,
        order_details_id: orderDetailsId
      },
      { headers: this.getAuthHeader() }
    );
  }

  sendStorageLicenseCallbackAndVerifyPayment(
    data: PaymentSuccessCallbackResponse,
    orderDetailsId: string
    ) {
    return this.httpClient.post(
      this.razorpayStorageLicenseCallbackUrl,
      {
        razorpay_order_id: data.razorpay_order_id,
        razorpay_payment_id: data.razorpay_payment_id,
        razorpay_signature: data.razorpay_signature,
        order_details_id: orderDetailsId
      },
      { headers: this.getAuthHeader() }
    );
  }

  deleteUnpaidCommonLicense(instituteSlug: string, orderPk: string) {
    return this.httpClient.delete(
      this.getDeleteUnpaidCommonLicenseUrl(instituteSlug, orderPk),
      { headers: this.getAuthHeader() }
    );
  }

  deleteUnpaidStorageLicense(instituteSlug: string, orderPk: string) {
    return this.httpClient.delete(
      this.getDeleteUnpaidStorageLicenseUrl(instituteSlug, orderPk),
      { headers: this.getAuthHeader() }
    );
  }

  getStorageLicenseCredentialsForRetryPayment(instituteSlug: string, orderPk: string) {
    return this.httpClient.get(
      this.getStorageLicenseCredentialsForRetryPaymentUrl(instituteSlug, orderPk),
      { headers: this.getAuthHeader() }
    );
  }

  getCommonLicenseCredentialsForRetryPayment(instituteSlug: string, orderPk: string) {
    return this.httpClient.get(
      this.getCommonLicenseCredentialsForRetryPaymentUrl(instituteSlug, orderPk),
      { headers: this.getAuthHeader() }
    );
  }

  // To get license purchase details of institue
  getInstituteOrderedLicense(instituteSlug: string, productType: string) {
    return this.httpClient.get(
      this.getInstituteLicenseOrderDetailsUrl(instituteSlug, productType),
      { headers: this.getAuthHeader() }
    );
  }

  // To get paid unexpired license details
  getLicenseExistsStatistics(instituteSlug: string) {
    return this.httpClient.get(
      this.getLicenseExistsStatisticsUrl(instituteSlug),
      { headers: this.getAuthHeader() }
    );
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
      { name },
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
    );
  }

  // To add class incharge
  addClassIncharge(invitee: string, classSlug: string) {
    return this.httpClient.post(
      this.addClassPermissionUrl,
      { invitee, class_slug: classSlug },
      { headers: this.getAuthHeader() }
    );
  }

  // Subject related methods
  createSubject(classSlug: string, name: string, type: string) {
    return this.httpClient.post(
      this.createSubjectUrl(classSlug),
      { name, type },
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
      { invitee, subject_slug: subjectSlug },
      { headers: this.getAuthHeader() }
    );
  }

  // To create institute section
  createClassSection(classSlug: string, name: string) {
    return this.httpClient.post(
      this.createSectionUrl(classSlug),
      { name },
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
      { invitee, section_slug: sectionSlug },
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

  createSubjectModule(
    subjectSlug: string,
    name: string,
    type: string
  ) {
    return this.httpClient.post(
      this.getCreateSubjectModuleUrl(subjectSlug),
      { name, type},
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
      { name: moduleName},
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

  addSubjectExternalLinkIntroductoryCourseContent(subjectSlug: string, data: any) {
    return this.httpClient.post(
      this.addSubjectIntroductoryCourseContentUrl(subjectSlug),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  uploadIntroductoryCourseContentMaterial(subjectSlug: string, data: any) {
    const formData = new FormData();
    formData.append('name', data.name);
    formData.append('view_key', data.view_key);
    formData.append('file', data.file);
    formData.append('content_type', data.content_type);

    if (data.content_type !== SUBJECT_INTRODUCTION_CONTENT_TYPE_REVERSE.LINK) {
      formData.append('can_download', data.can_download);
    }

    return this.httpClient.post(
      this.addSubjectIntroductoryCourseContentUrl(subjectSlug),
      formData,
      {
        headers: this.getAuthTokenHeader(),
        reportProgress: true,
        observe: 'events'
      }
    );
  }

  editSubjectCourseContent(data: any, subjectSlug: string, pk: string) {
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

  deleteSubjectIntroductoryContent(
    subjectSlug: string,
    pk: string
    ) {
    return this.httpClient.delete(
      this.getDeleteSubjectIntroductoryContentUrl(subjectSlug, pk),
      { headers: this.getAuthHeader() }
    );
  }

  addSubjectLecture(subjectSlug: string, data: any) {
    return this.httpClient.post(
      this.getAddSubjectLectureUrl(subjectSlug),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  deleteSubjectLecture(subjectSlug: string, lectureId: string) {
    return this.httpClient.delete(
      this.getDeleteSubjectLectureUrl(subjectSlug, lectureId),
      { headers: this.getAuthHeader() }
    );
  }

  editSubjectLecture(subjectSlug: string, lectureId: string, data) {
    return this.httpClient.patch(
      this.getEditSubjectLectureUrl(subjectSlug, lectureId),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  loadSubjectLectureContents(subjectSlug: string, lectureId: string) {
    return this.httpClient.get(
      this.getLoadSubjectLectureContentsUrl(subjectSlug, lectureId),
      { headers: this.getAuthHeader() }
    );
  }

  addLectureObjectiveOrUseCase(subjectSlug: string, lectureId: string, data) {
    return this.httpClient.post(
      this.getAddLectureObjectiveOrUseCaseUrl(subjectSlug, lectureId),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  deleteObjectiveOrUseCase(subjectSlug: string, id: string) {
    return this.httpClient.delete(
      this.getDeleteObjectiveOrUseCaseUrl(subjectSlug, id),
      { headers: this.getAuthHeader() }
    );
  }

  editObjectiveOrUseCase(subjectSlug: string, objectiveId: string, data) {
    return this.httpClient.patch(
      this.getEditLectureObjectiveOrUseCaseUrl(subjectSlug, objectiveId),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  addLectureAdditionalReadingOrUseCaseLink(subjectSlug: string, lectureId: string, data) {
    return this.httpClient.post(
      this.getAddLectureAdditionalReadingOrUseCaseLinkUrl(subjectSlug, lectureId),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  deleteAdditionalReadingOrUseCaseLink(subjectSlug: string, linkId: string) {
    return this.httpClient.delete(
      this.getDeleteAdditionalReadingOrUseCaseLinkUrl(subjectSlug, linkId),
      { headers: this.getAuthHeader() }
    );
  }

  editAdditionalReadingOrUseCaseLink(subjectSlug: string, linkId: string, data) {
    return this.httpClient.patch(
      this.getEditLectureAdditionalReadingOrUseCaseLinkUrl(subjectSlug, linkId),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  addExternalLinkCourseContent(subjectSlug: string, lectureId: string, data: any) {
    return this.httpClient.post(
      this.addLectureMaterialUrl(subjectSlug, lectureId),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  deleteLectureContent(subjectSlug: string, contentId: string) {
    return this.httpClient.delete(
      this.getDeleteLectureContentUrl(subjectSlug, contentId),
      { headers: this.getAuthHeader() }
    );
  }

  uploadMediaCourseContentMaterial(subjectSlug: string, lectureId: string, data: any) {
    const formData = new FormData();
    formData.append('name', data.name);
    formData.append('file', data.file);
    formData.append('content_type', data.content_type);

    if (data.content_type !== LECTURE_STUDY_MATERIAL_TYPES.EXTERNAL_LINK &&
        data.content_type !== LECTURE_STUDY_MATERIAL_TYPES.YOUTUBE_LINK) {
      formData.append('can_download', data.can_download);
    }

    return this.httpClient.post(
      this.addLectureMaterialUrl(subjectSlug, lectureId),
      formData,
      {
        headers: this.getAuthTokenHeader(),
        reportProgress: true,
        observe: 'events'
      }
    );
  }

  editSubjectLectureContent(subjectSlug: string, contentId: string, data) {
    return this.httpClient.patch(
      this.getEditLectureContentUrl(subjectSlug, contentId),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  addSubjectTest(instituteSlug: string, subjectSlug: string, data) {
    return this.httpClient.post(
      this.getAddSubjectTestUrl(instituteSlug, subjectSlug),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  getMinTestDetails(instituteSlug: string, subjectSlug: string, testSlug: string) {
    return this.httpClient.get(
      this.getMinTestDetailsUrl(instituteSlug, subjectSlug, testSlug),
      { headers: this.getAuthHeader() }
    );
  }

  getTestMinDetailsForQuestionCreation(subjectSlug: string, testSlug: string) {
    return this.httpClient.get(
      this.getTestMinDetailsForQuestionCreationUrl(subjectSlug, testSlug),
      { headers: this.getAuthHeader() }
    );
  }

  addTestQuestionSet(instituteSlug: string, subjectSlug: string, testSlug: string, data: any) {
    return this.httpClient.post(
      this.getAddTestQuestionSetUrl(instituteSlug, subjectSlug, testSlug),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  uploadFileQuestionPaper(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string,
    data: any
    ) {
    const formData = new FormData();
    formData.append('file', data.file);

    return this.httpClient.post(
      this.getUploadFileQuestionPaperUrl(instituteSlug, subjectSlug, testSlug, setId),
      formData,
      {
        headers: this.getAuthTokenHeader(),
        reportProgress: true,
        observe: 'events'
      },
    );
  }

  deleteTestFileUploadQuestionPaper(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string
    ) {
    return this.httpClient.delete(
      this.getDeleteTestFileUploadQuestionPaperUrl(instituteSlug, subjectSlug, testSlug, setId),
      { headers: this.getAuthHeader() }
    );
  }

  getTestSetQuestions(instituteSlug: string, subjectSlug: string, testSlug: string, setId: string) {
    return this.httpClient.get(
      this.getTestSetQuestionsUrl(instituteSlug, subjectSlug, testSlug, setId),
      { headers: this.getAuthHeader() }
    );
  }

  deleteQuestionSet(instituteSlug: string, subjectSlug: string, testSlug: string, setId: string) {
    return this.httpClient.delete(
      this.getDeleteQuestionSetUrl(instituteSlug, subjectSlug, testSlug, setId),
      { headers: this.getAuthHeader() }
    );
  }

  addTestConceptLabel(instituteSlug: string, subjectSlug: string, testSlug: string, data: any) {
    return this.httpClient.post(
      this.addTestConceptLabelUrl(instituteSlug, subjectSlug, testSlug),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  deleteConceptLabel(instituteSlug: string, subjectSlug: string, labelId: string) {
    return this.httpClient.delete(
      this.deleteTestConceptLabelUrl(instituteSlug, subjectSlug, labelId),
      { headers: this.getAuthHeader() }
    );
  }

  addTestQuestionSection(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string,
    data: any
    ) {
    return this.httpClient.post(
      this.addTestQuestionSectionUrl(instituteSlug, subjectSlug, testSlug, setId),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  addImageTestQuestion(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string,
    setSectionId: string,
    data: any
    ) {
    const formData = new FormData();
    formData.append('file', data.file);
    formData.append('marks', data.marks);

    if (data.concept_label){
      formData.append('concept_label', data.concept_label);
    }

    if (data.text) {
      formData.append('text', data.text);
    }

    return this.httpClient.post(
      this.addImageTestQuestionUrl(instituteSlug, subjectSlug, testSlug, setId, setSectionId),
      formData,
      {
        headers: this.getAuthTokenHeader(),
        reportProgress: true,
        observe: 'events'
      }
    );
  }

  deleteImageTestQuestion(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string,
    questionId: string,
    ) {
    return this.httpClient.delete(
      this.deleteImageTestQuestionUrl(instituteSlug, subjectSlug, testSlug, setId, questionId),
      { headers: this.getAuthHeader() }
    );
  }

  editImageTestQuestion(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string,
    questionId: string,
    data: any
    ) {
    return this.httpClient.patch(
      this.editImageTestQuestionUrl(instituteSlug, subjectSlug, testSlug, setId, questionId),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  editQuestionSet(
    instituteSlug: string,
    subjectSlug: string,
    testSlug: string,
    setId: string,
    data: any
    ) {
    return this.httpClient.patch(
      this.editQuestionSetUrl(instituteSlug, subjectSlug, testSlug, setId),
      data,
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

  studentJoinInstitute(instituteSlug: string, data: any) {
    return this.httpClient.post(
      this.getStudentJoinInstituteUrl(instituteSlug),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  getAllStudentCourses() {
    return this.httpClient.get(
      this.allStudentCoursesUrl,
      { headers: this.getAuthHeader() }
    );
  }

  getClassStudentsList(
    instituteSlug: string,
    classSlug: string,
    studentType: string
    ) {
    return this.httpClient.get(
      this.getClassStudentsListUrl(
        instituteSlug,
        classSlug,
        studentType
      ),
      { headers: this.getAuthHeader() }
    );
  }

  inviteStudentToClass(
    instituteSlug: string,
    classSlug: string,
    data: any
  ) {
    return this.httpClient.post(
      this.getInviteStudentToClassUrl(
        instituteSlug,
        classSlug
      ),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  getSubjectStudentsList(
    instituteSlug: string,
    classSlug: string,
    subjectSlug: string,
    studentType: string
    ) {
    return this.httpClient.get(
      this.getSubjectStudentsListUrl(
        instituteSlug,
        classSlug,
        subjectSlug,
        studentType
      ),
      { headers: this.getAuthHeader() }
    );
  }

  inviteStudentToSubject(
    instituteSlug: string,
    classSlug: string,
    subjectSlug: string,
    data: any
  ) {
    return this.httpClient.post(
      this.getInviteStudentToSubjectUrl(
        instituteSlug,
        classSlug,
        subjectSlug
      ),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  getCoursePeers(instituteSlug: string, subjectSlug: string) {
    return this.httpClient.get(
      this.getCoursePeersUrl(instituteSlug, subjectSlug),
      { headers: this.getAuthHeader() }
    );
  }

  bookmarkInstituteCourse(subjectId: string) {
    return this.httpClient.post(
      this.bookmarkCourseUrl,
      { subject_id: subjectId },
      { headers: this.getAuthHeader() }
    );
  }

  askQuestionInCourseContent(
    instituteSlug: string,
    subjectSlug: string,
    courseContentId: string,
    data: any
  ) {
    return this.httpClient.post(
      this.getAskQuestionInCourseContentUrl(
        instituteSlug,
        subjectSlug,
        courseContentId
      ),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  loadAllInstituteSubjectCourseContentQuestions(
    instituteSlug: string,
    subjectSlug: string,
    courseContentId: string,
  ) {
    return this.httpClient.get(
      this.getLoadAllInstituteSubjectCourseContentQuestionsUrl(
        instituteSlug,
        subjectSlug,
        courseContentId
      ),
      { headers: this.getAuthHeader() }
    );
  }

  loadAnswerOfInstituteCourseQuestion(
    instituteSlug: string,
    subjectSlug: string,
    questionId: string
  ) {
    return this.httpClient.get(
      this.getLoadAnswerOfInstituteCourseQuestionUrl(
        instituteSlug,
        subjectSlug,
        questionId
      ),
      { headers: this.getAuthHeader() }
    );
  }

  answerQuestionOfInstituteCourseContent(
    instituteSlug: string,
    subjectSlug: string,
    questionId: string,
    data: any
  ) {
    return this.httpClient.post(
      this.getAnswerQuestionOfInstituteCourseContentUrl(
        instituteSlug,
        subjectSlug,
        questionId
      ),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  upvoteDownvoteInstituteCourseContentQuestion(
    instituteSlug: string,
    subjectSlug: string,
    questionId: string,
    data: any
  ) {
    return this.httpClient.post(
      this.getUpvoteDownvoteInstituteCourseContentQuestionUrl(
        instituteSlug,
        subjectSlug,
        questionId
      ),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  upvoteDownvoteInstituteCourseContentAnswer(
    instituteSlug: string,
    subjectSlug: string,
    answerId: string,
    data: any
  ) {
    return this.httpClient.post(
      this.getUpvoteDownvoteInstituteCourseContentAnswerUrl(
        instituteSlug,
        subjectSlug,
        answerId
      ),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  deleteInstituteCourseContentAnswer(
    subjectSlug: string,
    answerId: string
  ) {
    return this.httpClient.delete(
      this.getDeleteInstituteCourseContentAnswerUrl(subjectSlug, answerId),
      { headers: this.getAuthHeader() }
    );
  }

  pinUnpinInstituteCourseContentAnswer(answerId: string, data: any) {
    return this.httpClient.patch(
      this.getPinUnpinInstituteCourseContentAnswerUrl(answerId),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  editInstituteCourseContentAnswer(
    instituteSlug: string,
    subjectSlug: string,
    answerId: string,
    data: any
  ) {
    return this.httpClient.patch(
      this.getEditInstituteCourseContentAnswerUrl(
        instituteSlug,
        subjectSlug,
        answerId
      ),
      data,
      { headers: this.getAuthHeader() }
    );
  }

  editInstituteCourseContentQuestion(
    instituteSlug: string,
    subjectSlug: string,
    questionId: string,
    data: any
  ) {
    return this.httpClient.patch(
      this.getEditInstituteCourseContentQuestionUrl(
        instituteSlug,
        subjectSlug,
        questionId
      ),
      data,
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
