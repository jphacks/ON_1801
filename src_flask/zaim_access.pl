#!/usr/bin/perl

use strict;
use warnings;

use OAuth::Lite::Consumer;
use OAuth::Lite::Token;


my $consumer_key    = '5a16dc78b738134b766719315527fd7b639ac87f';
my $consumer_secret = '9b53494758fb485c09e0587d4694c49ac1ad6e7f';

my $consumer = OAuth::Lite::Consumer->new(
    consumer_key          => $consumer_key,
    consumer_secret       => $consumer_secret,
    site                  => q{https://api.zaim.net},
    request_token_path    => q{https://api.zaim.net/v2/auth/request},
    access_token_path     => q{https://api.zaim.net/v2/auth/access},
    authorize_path        => q{https://www.zaim.net/users/auth},
    );

my $request_token = $consumer->get_request_token(
    callback_url => 'http://google.com/' #適当なURLを入れておく
    ) or die $consumer->errstr."\n";;

     
#print "request token:$request_token\n;";

my $url = $consumer->url_to_authorize(
    token   => $request_token,
    );


print "$url\n";
print "上記URLにアクセス後、Verifierを入力してください:\n";

my $verifier = <STDIN>;
$verifier =~ s/\x0D?\x0A$//g; #cygwinの場合
#chomp $verifier             #cygwin以外

print "verifier:$verifier\n";

my $access_token = $consumer->get_access_token(
    token       => $request_token,
    verifier    => $verifier,
    ) or die $consumer->errstr;;

print "access token:       $access_token->{'token'}\n";
print "access_token_secret:$access_token->{'secret'}\n";
