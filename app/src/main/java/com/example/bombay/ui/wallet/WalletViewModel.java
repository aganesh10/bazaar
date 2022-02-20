package com.example.bombay.ui.wallet;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class WalletViewModel extends ViewModel {

    private final MutableLiveData<String> mText;

    public WalletViewModel() {
        mText = new MutableLiveData<>();
//        mText.setValue("STFU");
    }

    public LiveData<String> getText() {
        return mText;
    }
}