export interface SubjectInchargeDetails {
  id?: number;
  email?: string;
  name?: string;
}

export interface InstituteSubjectDetails {
  id: number;
  name: string;
  subject_slug: string;
  type: string;
  created_on: string;
  has_subject_perm: boolean;
  subject_incharges: SubjectInchargeDetails[]
}

export interface SubjectPermittedUserDetails {
  id: number;
  email: string;
  name?: string;
  invitee_id: string;
  inviter_name?: string;
  inviter_email?: string;
  created_on: string;
  image?: string;
}


export interface ViewDetails {
  key: {
    name: string;
    count: number;
    number?: number;
    weeks?: Array<number>;
  }
}


export interface SubjectCourseMinDetails {
  view_order: Array<string>;
  view_details: ViewDetails;
};

export interface SubjectCourseViewDetails {
  MI: number;
  CO: number;
}

export interface StorageStatistics {
  total_storage: number;
  storage_used: number;
}

export interface StudyMaterialDetails {
  id: number;
  order: number;
  target_date?: string;
  title: string;
  uploaded_on: string;
  view: string;
  content_type: string;
  description?: string;
  week?: number;
  data: {
    id?: number;
    url?: string;         // For external link
    file?: string;        // For image and video file download
    bit_rate?: number;    // For video file
    duration?: number;
    stream_file?: string;
    error_transcoding?: boolean;
    size?: number;
    can_download?: boolean;
    total_pages?: number; // For pdf
  };
}

export interface CreateSubjectModuleResponse {
  name: string;
  view: string;
  number?: number;
  weeks: Array<number>;
}


export interface InstructorDetails {
  id: number;
  name?: string;
  email?: string;
  image?: string;
}


export interface SubjectPreviewCourseMinDetails {
  instructors: Array<InstructorDetails>;
  view_order: Array<string>;
  view_details: ViewDetails;
};

export interface StudyMaterialPreviewDetails {
  id: number;
  order: number;
  target_date?: string;
  title: string;
  uploaded_on: string;
  view: string;
  content_type: string;
  description?: string;
  week?: number;
  data: {
    id?: number;
    url?: string;         // For external link
    file?: string;        // For image and video file download
    bit_rate?: number;    // For video file
    duration?: number;
    stream_file?: string;
    error_transcoding?: boolean;
    size?: number;
    can_download?: boolean;
    total_pages?: number; // For pdf
  };
}

export interface SubjectPeerDetails {
  name: string;
  user_id: number;
  enrollment_no?: string;
  image: string;
}

export interface SubjectPeersResponse {
  view_order: Array<string>;
  instructors: SubjectPeerDetails[];
  students: SubjectPeerDetails[];
}
