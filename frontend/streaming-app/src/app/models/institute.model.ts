export interface TeacherInstitutesMinDetailInterface {
  id: number;
  name: string;
  country: string;
  institute_category: string;
  type: string;
  created_date: string;
  institute_slug: string;
  role: string;
  institute_profile: {
    motto: string;
    email: string;
    phone: string;
    website_url: string;
    state: string;
    recognition: string;
  };
  institute_logo: {
    image: string;
  };
  institute_statistics: {
    no_of_students: number;
    no_of_faculties: number;
    no_of_staff: number;
    no_of_admin: number;
  };
}


export interface InstituteCreatedEvent {
  status: boolean;
  url: string;
  type: string;
}


export interface StatusResponse {
  status: string;
}


export interface UserProfileDetailsExistsStatus {
  status: boolean;
}

export interface StudentInstitutesMinDetailInterface {
  id: number;
  name: string;
  country: string;
  institute_category: string;
  type: string;
  created_date: string;
  institute_slug: string;
  role: string;
  institute_profile: {
    motto: string;
    email: string;
    phone: string;
    website_url: string;
    state: string;
    recognition: string;
  };
  institute_logo: {
    image: string;
  };
  institute_statistics: {
    no_of_students: number;
    no_of_faculties: number;
    no_of_staff: number;
    no_of_admin: number;
  };
}

export interface StudentGetInstitutesListInterface {
  active_institutes: StudentInstitutesMinDetailInterface[];
  invited_institutes: StudentInstitutesMinDetailInterface[];
}

export interface StudentConfirmProfileDataInterface {
  first_name: string;
  last_name: string;
  gender: string;
  date_of_birth: string;
}
