export interface UserProfileDetails {
  id: number;
  email: string;
  username: string;
  created_date: string;
  user_profile: {
    first_name: string;
    last_name: string;
    gender: string;
    phone: string;
    country: string;
    date_of_birth: string;
    primary_language: string;
    secondary_language: string;
    tertiary_language: string;
  };
  profile_pictures: {
    id: number;
    image: string;
    uploaded_on: string;
    public_profile_picture: boolean;
    class_profile_picture: boolean;
  };
}

export interface DeletedCurrentPictureResponse {
  deleted: boolean;
  class_profile_picture_deleted: boolean;
  public_profile_picture_deleted: boolean;
}

export interface ImageUploadResponse {
  type: number;
  loaded: number;
  total: number;
  body: {
    id: string;
    image: string;
    class_profile_picture: boolean;
    public_profile_picture: boolean;
    uploaded_on: string;
  };
  headers: {
    ok: boolean;
    status: number;
    statusText: string;
    type: number;
    url: string;
  };
}
