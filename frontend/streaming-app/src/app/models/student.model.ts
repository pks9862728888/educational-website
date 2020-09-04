export interface InstituteStudentMinDetails {
  id: number;
  invitee_email: string;
  first_name: string;
  last_name: string;
  gender: string;
  date_of_birth: string;
  enrollment_no: string;
  registration_no: string;
  created_on: string;
  class_name: string;
  is_banned?: boolean;
  image: string;
};


export interface StudentCourseListViewOrder {
  name: string;
  institute_slug: string;
}


export interface StudentCourseDetails {
  institute_slug: string;
  class_slug: string;
  subject_slug: string;
  subject_name: string;
  subject_description: string;
  subject_id: number;
  BOOKMARKED: boolean;
}


export interface StudentAllCoursesList {
  view_order: StudentCourseListViewOrder[];
  courses: {
    string: StudentCourseDetails;
  };
  class_names: {}
  favourite_courses: {
    string: StudentCourseDetails;
  };
}
