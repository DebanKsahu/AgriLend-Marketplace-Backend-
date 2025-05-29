from fastapi import status,HTTPException

user_not_found_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
)
user_profile_not_found_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
)
credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
)