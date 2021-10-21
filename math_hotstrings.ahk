#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.


; Made by interestingbookstore
; Github: https://github.com/interestingbookstore/randomstuff

; You can toggle the shortcut by pressing alt+1
toggle:= 0
!1::
    toggle := !toggle
    return


#if toggle = 1
    :*?:+-::±
    :*?:-::−
    :*?:*::×
    :*?:/::÷

    :*?:sqrt::√
    :*?:degree::°
    :*?:normalangle::∠
    :*?:rightangle::∟
    :*?:triangle::Δ

    :*?:times::×
    :*?:divided by::÷
    :*?:square root of::√

    :*?:delta::Δ
    :*?:pi::π

    :*?:^^0::₀
    :*?:^^1::₁
    :*?:^^2::₂
    :*?:^^3::₃
    :*?:^^4::₄
    :*?:^^5::₅
    :*?:^^6::₆
    :*?:^^7::₇
    :*?:^^8::₈
    :*?:^^9::₉
    :*?:^^+::₊
    :*?:^^−::₋
    :*?:^^=::₌
    :*?:^^(::₍
    :*?:^^)::₎


    :*?:^0::⁰
    :*?:^1::¹
    :*?:^2::²
    :*?:^3::³
    :*?:^4::⁴
    :*?:^5::⁵
    :*?:^6::⁶
    :*?:^7::⁷
    :*?:^8::⁸
    :*?:^9::⁹
    :*?:^+::⁺
    :*?:^-::⁻
    :*?:^=::⁼
    :*?:^(::⁽
    :*?:^)::⁾
