export interface LoginUser {
    username: string;
    password: string;
}

export interface LoginResponse {
    access_token: string;
    expires_in: number;
    refresh_expires_in: number;
    refresh_token: string;
    token_type: string;
}