#!/usr/bin/perl

use strict;
use warnings;

use OAuth::Lite::Consumer;
use OAuth::Lite::Token;


my $consumer_key    = $ENV{ZAIM_KEY};
my $consumer_secret = $ENV{ZAIM_SECRET};

my $consumer = OAuth::Lite::Consumer->new(
    consumer_key          => $consumer_key,
    consumer_secret       => $consumer_secret,
    site                  => q{https://api.zaim.net},
    request_token_path    => q{https://api.zaim.net/v2/auth/request},
    access_token_path     => q{https://api.zaim.net/v2/auth/access},
    authorize_path        => q{https://auth.zaim.net/users/auth},
    );

my $request_token = $consumer->get_request_token(
    callback_url => 'https://api.zaim.net' #適当なURLを入れておく
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
