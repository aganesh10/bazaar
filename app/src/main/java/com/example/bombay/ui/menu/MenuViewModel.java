package com.example.bombay.ui.menu;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class MenuViewModel extends ViewModel {

    private final MutableLiveData<String> mText;

    public MenuViewModel() {
        mText = new MutableLiveData<>();
//        mText.setValue("YO");
    }

    public LiveData<String> getText() {
        return mText;
    }
}