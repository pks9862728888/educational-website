export interface InstituteStudentMinDetails {
  id: number;
  invitee_email: string;
  first_name: string;
  last_name: string;
  enrollment_no: string;
  registration_no: string;
  created_on: string;
  class_name: string;
  is_banned?: boolean;
  image: string;
};
