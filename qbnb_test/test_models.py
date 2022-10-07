from qbnb.backend_functions import create_listing


def test_r1_1_create_listing():
    '''
    Testing R4-1 and R4-2. Title must be alhpanumeric and no space allowed as
      suffix or prefix. Tilte must be inbetween length of 20 - 80
    '''
    # title is not alhpanumeric so it should return false
    assert create_listing("House listing 1!",
                          "This is a great house! Buy before somoene else does!",  1000, 1) is False
    # title is too short
    assert create_listing(
        "small", "This is a great house! Buy before somoene else does!",  1000, 1) is False
    # title is too long
    assert create_listing("this is a very long title that is going to be longer than 80\
       characters long and should make the function return false.",
                          "This is a great house! Buy before somoene else does!",  1000, 1) is False
    # this is a proper title
    assert create_listing("House listing 1",
                          "This is a great house! Buy before somoene else does!",  1000, 1) is True
